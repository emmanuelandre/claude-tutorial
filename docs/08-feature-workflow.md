# Feature Development Workflow

Complete walkthrough of implementing a feature from start to finish.

## Overview

This guide demonstrates the practical application of the AI-first workflow with a real example: adding a password reset feature.

## Feature: Password Reset

### Initial Request

```
"I need to implement password reset functionality. Users should be able to:
1. Request a password reset via email
2. Receive a time-limited reset link
3. Set a new password using the link
4. Be redirected to login after successful reset

Include comprehensive E2E tests and follow our CLAUDE.md conventions."
```

## Step-by-Step Implementation

### Phase 1: Planning

**Human → Claude:**
```
"Before implementing, let's plan the password reset feature:

1. What database schema changes do we need?
2. What API endpoints are required?
3. What security considerations should we address?
4. What edge cases should we handle?

Provide a detailed implementation plan."
```

**Claude → Human:**
```markdown
## Implementation Plan: Password Reset

### Database Schema
- New table: `password_reset_tokens`
  - Columns: id, user_id, token (hashed), expires_at, used_at, created_at
  - Indexes: token, user_id, expires_at

### API Endpoints
1. POST /api/v1/auth/forgot-password
   - Input: { email }
   - Creates token, sends email
   - Returns: 200 (always, to prevent email enumeration)

2. POST /api/v1/auth/reset-password
   - Input: { token, new_password }
   - Validates token, updates password
   - Returns: 200 or 400

3. GET /api/v1/auth/verify-reset-token/:token
   - Validates token without using it
   - Returns: 200 if valid, 400 if invalid/expired

### Security Considerations
- Hash tokens before storing
- Tokens expire after 1 hour
- One-time use only
- Rate limit forgot-password endpoint (max 3/hour per IP)
- Strong password requirements
- Don't reveal if email exists in database

### Edge Cases
- Expired tokens
- Already used tokens
- Invalid tokens
- Non-existent email
- User deleted after token created
- Multiple concurrent reset requests
```

**Human Review:**
✅ Approve plan or request modifications

### Phase 2: Database Migration

**Human → Claude:**
```
"Create the database migration for password reset tokens following the approved plan."
```

**Claude creates:**

```sql
-- migrations/007_password_reset_tokens.up.sql

CREATE TABLE password_reset_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_password_reset_tokens_user
  ON password_reset_tokens(user_id);
CREATE INDEX idx_password_reset_tokens_hash
  ON password_reset_tokens(token_hash);
CREATE INDEX idx_password_reset_tokens_expires
  ON password_reset_tokens(expires_at);

-- migrations/007_password_reset_tokens.down.sql

DROP TABLE IF EXISTS password_reset_tokens;
```

**Human Review:**
- Verify schema matches plan
- Check foreign key constraints
- Confirm indexes are appropriate

**Human executes:**
```bash
psql -d mydb -f migrations/007_password_reset_tokens.up.sql
```

### Phase 3: Repository Layer

**Human → Claude:**
```
"Implement the repository methods for password reset tokens in Go.
Include: CreateResetToken, GetResetToken, MarkTokenUsed, DeleteExpiredTokens."
```

**Claude creates:**

```go
// internal/repository/password_reset_repository.go

package repository

import (
    "context"
    "crypto/rand"
    "crypto/sha256"
    "database/sql"
    "encoding/hex"
    "fmt"
    "time"
)

type PasswordResetRepository struct {
    db *sql.DB
}

type PasswordResetToken struct {
    ID        int
    UserID    int
    TokenHash string
    ExpiresAt time.Time
    UsedAt    *time.Time
    CreatedAt time.Time
}

func (r *PasswordResetRepository) CreateResetToken(
    ctx context.Context,
    userID int,
) (string, error) {
    // Generate secure random token
    tokenBytes := make([]byte, 32)
    if _, err := rand.Read(tokenBytes); err != nil {
        return "", fmt.Errorf("failed to generate token: %w", err)
    }
    token := hex.EncodeToString(tokenBytes)

    // Hash token for storage
    hash := sha256.Sum256([]byte(token))
    tokenHash := hex.EncodeToString(hash[:])

    // Insert with 1 hour expiration
    expiresAt := time.Now().Add(1 * time.Hour)
    _, err := r.db.ExecContext(
        ctx,
        `INSERT INTO password_reset_tokens (user_id, token_hash, expires_at)
         VALUES ($1, $2, $3)`,
        userID, tokenHash, expiresAt,
    )

    if err != nil {
        return "", fmt.Errorf("failed to create reset token: %w", err)
    }

    return token, nil  // Return unhashed token for email
}

func (r *PasswordResetRepository) GetResetToken(
    ctx context.Context,
    token string,
) (*PasswordResetToken, error) {
    // Hash the provided token
    hash := sha256.Sum256([]byte(token))
    tokenHash := hex.EncodeToString(hash[:])

    var resetToken PasswordResetToken
    err := r.db.QueryRowContext(
        ctx,
        `SELECT id, user_id, token_hash, expires_at, used_at, created_at
         FROM password_reset_tokens
         WHERE token_hash = $1`,
        tokenHash,
    ).Scan(
        &resetToken.ID,
        &resetToken.UserID,
        &resetToken.TokenHash,
        &resetToken.ExpiresAt,
        &resetToken.UsedAt,
        &resetToken.CreatedAt,
    )

    if err == sql.ErrNoRows {
        return nil, ErrTokenNotFound
    }
    if err != nil {
        return nil, fmt.Errorf("failed to get reset token: %w", err)
    }

    return &resetToken, nil
}

func (r *PasswordResetRepository) MarkTokenUsed(
    ctx context.Context,
    token string,
) error {
    hash := sha256.Sum256([]byte(token))
    tokenHash := hex.EncodeToString(hash[:])

    _, err := r.db.ExecContext(
        ctx,
        `UPDATE password_reset_tokens
         SET used_at = NOW()
         WHERE token_hash = $1`,
        tokenHash,
    )

    return err
}
```

**Human Review:**
- Verify token generation is cryptographically secure
- Confirm hashing is done correctly
- Check error handling
- Verify expiration logic

### Phase 4: API Implementation

**Human → Claude:**
```
"Implement the password reset API endpoints with proper validation,
error handling, and rate limiting."
```

**Claude creates:**

```go
// internal/handlers/password_reset_handler.go

func (h *AuthHandler) ForgotPassword(w http.ResponseWriter, r *http.Request) {
    var req struct {
        Email string `json:"email"`
    }

    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "Invalid request")
        return
    }

    // Validate email format
    if !isValidEmail(req.Email) {
        respondError(w, http.StatusBadRequest, "Invalid email format")
        return
    }

    // Find user (don't reveal if exists)
    user, err := h.userRepo.FindByEmail(r.Context(), req.Email)
    if err == nil && user != nil {
        // User exists, create reset token
        token, err := h.resetRepo.CreateResetToken(r.Context(), user.ID)
        if err != nil {
            log.Printf("Failed to create reset token: %v", err)
            // Continue to prevent timing attacks
        } else {
            // Send email
            resetURL := fmt.Sprintf("https://example.com/reset-password?token=%s", token)
            if err := h.emailService.SendPasswordReset(user.Email, resetURL); err != nil {
                log.Printf("Failed to send reset email: %v", err)
            }
        }
    }

    // Always return success (prevent email enumeration)
    respondJSON(w, http.StatusOK, map[string]string{
        "message": "If the email exists, a reset link has been sent",
    })
}

func (h *AuthHandler) ResetPassword(w http.ResponseWriter, r *http.Request) {
    var req struct {
        Token       string `json:"token"`
        NewPassword string `json:"new_password"`
    }

    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "Invalid request")
        return
    }

    // Validate password strength
    if err := validatePassword(req.NewPassword); err != nil {
        respondError(w, http.StatusBadRequest, err.Error())
        return
    }

    // Get and validate token
    resetToken, err := h.resetRepo.GetResetToken(r.Context(), req.Token)
    if err != nil {
        respondError(w, http.StatusBadRequest, "Invalid or expired token")
        return
    }

    // Check if expired
    if time.Now().After(resetToken.ExpiresAt) {
        respondError(w, http.StatusBadRequest, "Token has expired")
        return
    }

    // Check if already used
    if resetToken.UsedAt != nil {
        respondError(w, http.StatusBadRequest, "Token has already been used")
        return
    }

    // Update password
    hashedPassword, err := bcrypt.GenerateFromPassword(
        []byte(req.NewPassword),
        bcrypt.DefaultCost,
    )
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to reset password")
        return
    }

    err = h.userRepo.UpdatePassword(r.Context(), resetToken.UserID, string(hashedPassword))
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to reset password")
        return
    }

    // Mark token as used
    if err := h.resetRepo.MarkTokenUsed(r.Context(), req.Token); err != nil {
        log.Printf("Failed to mark token as used: %v", err)
    }

    respondJSON(w, http.StatusOK, map[string]string{
        "message": "Password reset successfully",
    })
}
```

**Human Review:**
- Security measures in place?
- Error messages don't leak information?
- Rate limiting configured?
- Logging appropriate?

### Phase 5: E2E Tests

**Human → Claude:**
```
"Write comprehensive E2E tests for password reset API covering
all happy paths and error scenarios."
```

**Claude creates:**

```javascript
// tests/e2e/api/password-reset.cy.js

describe('API: Password Reset', () => {
  const testEmail = 'test@example.com'
  let resetToken

  before(() => {
    // Create test user
    cy.request('POST', '/api/v1/auth/register', {
      email: testEmail,
      password: 'OldPass123!',
      name: 'Test User'
    })
  })

  describe('POST /api/v1/auth/forgot-password', () => {
    it('sends reset email for existing user', () => {
      cy.request('POST', '/api/v1/auth/forgot-password', {
        email: testEmail
      }).then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body.message).to.include('reset link has been sent')
      })

      // Verify token was created in database
      cy.task('db:query', {
        query: 'SELECT * FROM password_reset_tokens WHERE user_id = (SELECT id FROM users WHERE email = $1) ORDER BY created_at DESC LIMIT 1',
        values: [testEmail]
      }).then((result) => {
        expect(result.rows).to.have.length(1)
        const token = result.rows[0]
        expect(token.expires_at).to.be.gt(new Date())
      })
    })

    it('returns success even for non-existent email', () => {
      cy.request('POST', '/api/v1/auth/forgot-password', {
        email: 'nonexistent@example.com'
      }).then((response) => {
        expect(response.status).to.eq(200)
      })
    })

    it('returns 400 for invalid email format', () => {
      cy.request({
        method: 'POST',
        url: '/api/v1/auth/forgot-password',
        body: { email: 'invalid-email' },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(400)
      })
    })
  })

  describe('POST /api/v1/auth/reset-password', () => {
    beforeEach(() => {
      // Get valid reset token
      cy.task('db:query', {
        query: `
          INSERT INTO password_reset_tokens (user_id, token_hash, expires_at)
          VALUES (
            (SELECT id FROM users WHERE email = $1),
            encode(sha256('test-token'), 'hex'),
            NOW() + INTERVAL '1 hour'
          )
        `,
        values: [testEmail]
      })
      resetToken = 'test-token'
    })

    it('resets password with valid token', () => {
      const newPassword = 'NewPass123!'

      cy.request('POST', '/api/v1/auth/reset-password', {
        token: resetToken,
        new_password: newPassword
      }).then((response) => {
        expect(response.status).to.eq(200)
      })

      // Verify can login with new password
      cy.request('POST', '/api/v1/auth/login', {
        email: testEmail,
        password: newPassword
      }).then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body).to.have.property('token')
      })

      // Verify token is marked as used
      cy.task('db:query', {
        query: 'SELECT used_at FROM password_reset_tokens WHERE token_hash = encode(sha256($1), \'hex\')',
        values: ['test-token']
      }).then((result) => {
        expect(result.rows[0].used_at).to.not.be.null
      })
    })

    it('rejects weak password', () => {
      cy.request({
        method: 'POST',
        url: '/api/v1/auth/reset-password',
        body: {
          token: resetToken,
          new_password: 'weak'
        },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(400)
        expect(response.body.error).to.include('Password must be')
      })
    })

    it('rejects expired token', () => {
      // Create expired token
      cy.task('db:query', {
        query: `
          INSERT INTO password_reset_tokens (user_id, token_hash, expires_at)
          VALUES (
            (SELECT id FROM users WHERE email = $1),
            encode(sha256('expired-token'), 'hex'),
            NOW() - INTERVAL '1 hour'
          )
        `,
        values: [testEmail]
      })

      cy.request({
        method: 'POST',
        url: '/api/v1/auth/reset-password',
        body: {
          token: 'expired-token',
          new_password: 'NewPass123!'
        },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(400)
        expect(response.body.error).to.include('expired')
      })
    })

    it('rejects already used token', () => {
      // Mark token as used
      cy.task('db:query', {
        query: `UPDATE password_reset_tokens
                SET used_at = NOW()
                WHERE token_hash = encode(sha256($1), 'hex')`,
        values: [resetToken]
      })

      cy.request({
        method: 'POST',
        url: '/api/v1/auth/reset-password',
        body: {
          token: resetToken,
          new_password: 'NewPass123!'
        },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(400)
        expect(response.body.error).to.include('already been used')
      })
    })

    it('rejects invalid token', () => {
      cy.request({
        method: 'POST',
        url: '/api/v1/auth/reset-password',
        body: {
          token: 'invalid-token',
          new_password: 'NewPass123!'
        },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(400)
        expect(response.body.error).to.include('Invalid')
      })
    })
  })
})
```

**Human:** Run tests and verify all pass

```bash
npm run test:e2e:api
```

### Phase 6: Frontend Implementation

**Human → Claude:**
```
"Create React components for forgot password and reset password pages."
```

**Claude creates components:**

- `ForgotPasswordPage.jsx`
- `ResetPasswordPage.jsx`
- `PasswordStrengthIndicator.jsx`

(Full component code similar to previous examples)

### Phase 7: UI E2E Tests

**Human → Claude:**
```
"Write UI E2E tests for the password reset flow."
```

**Claude creates:**

```javascript
// tests/e2e/ui/password-reset.cy.js

describe('UI: Password Reset', () => {
  it('completes full password reset flow', () => {
    // 1. Request reset
    cy.visit('/forgot-password')
    cy.get('[data-test="email-input"]').type('test@example.com')
    cy.get('[data-test="submit-button"]').click()

    cy.contains('reset link has been sent').should('be.visible')

    // 2. Get reset token from database
    cy.task('db:getLatestResetToken', 'test@example.com')
      .then((token) => {
        // 3. Visit reset page
        cy.visit(`/reset-password?token=${token}`)

        cy.get('[data-test="password-input"]').type('NewPass123!')
        cy.get('[data-test="confirm-password-input"]').type('NewPass123!')

        // Verify strength indicator
        cy.get('[data-test="password-strength"]')
          .should('contain', 'Strong')

        cy.get('[data-test="submit-button"]').click()

        // 4. Verify success and redirect
        cy.url().should('include', '/login')
        cy.contains('Password reset successfully').should('be.visible')

        // 5. Login with new password
        cy.get('[data-test="email-input"]').type('test@example.com')
        cy.get('[data-test="password-input"]').type('NewPass123!')
        cy.get('[data-test="submit-button"]').click()

        cy.url().should('include', '/dashboard')
      })
  })
})
```

**Human:** Run tests and verify all pass

### Phase 8: Documentation

**Claude updates:**
- API documentation
- README with new endpoints
- Code comments

### Phase 9: Code Review

**Human reviews:**
- Security implementation
- Error handling
- Test coverage
- Code quality
- Documentation

### Phase 10: Commit and Deploy

```bash
# Create feature branch
git checkout -b feature/password-reset

# Commit
git add .
git commit -m "feat(auth): add password reset functionality

- Add password_reset_tokens table
- Implement forgot-password and reset-password endpoints
- Add comprehensive E2E tests (API and UI)
- Include rate limiting and security measures
- Update API documentation"

# Push and create PR
git push -u origin feature/password-reset
gh pr create --title "feat: Add password reset functionality" \
  --body "Implements secure password reset flow with email verification"
```

## Summary

**Time Investment:**
- Specification: 15 minutes
- Implementation: 2 hours (AI-executed)
- Review & Testing: 30 minutes
- **Total: ~3 hours**

**Traditional Approach:**
- Same feature: 1-2 days

**Quality Achieved:**
- ✅ Comprehensive E2E tests
- ✅ Security best practices
- ✅ Complete documentation
- ✅ All edge cases handled

---

**Prev:** [AI-First Workflow](./07-ai-first-workflow.md) | **Next:** [Real-World Examples](./09-real-world-examples.md)

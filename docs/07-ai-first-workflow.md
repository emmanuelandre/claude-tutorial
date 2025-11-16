# AI-First Development Workflow

The systematic process for building features with AI-first development.

## Core Principle

**AI executes 100%, Humans validate 100%**

This isn't about AI doing half the work. It's about:
- AI handles all execution (coding, testing, docs)
- Humans handle all validation (review, approve, decide)
- Clear handoff points between AI and human
- Systematic quality gates

## The 10-Step Workflow

### Step 1: Specification

**Human:** Write detailed specification

```markdown
## Feature: User Profile Editing

### User Story
As a logged-in user, I want to edit my profile information
so that I can keep my account details up to date.

### Requirements
- Users can update: name, email, bio, avatar
- Email must be unique across all users
- Email changes require verification
- Changes persist to database
- Optimistic UI updates
- Handle network errors gracefully

### UI Mockup
[Link to Figma/screenshot]

### API Contract
PUT /api/v1/users/:id
Body: { name, email, bio, avatar_url }
Returns: 200 { user } or 400 { error }

### Success Criteria
- Form validates input before submission
- Database updates correctly
- Email verification flow works
- Error messages are clear
- All E2E tests pass
```

**Deliverable:** Detailed specification document

### Step 2: Database Schema

**AI:** Design and implement database schema

```sql
-- Migration: 003_user_profiles.up.sql

-- Add bio and avatar to users table
ALTER TABLE users
  ADD COLUMN bio TEXT,
  ADD COLUMN avatar_url VARCHAR(500),
  ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;

-- Table for email verification tokens
CREATE TABLE email_verification_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  token VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_verification_tokens_user
  ON email_verification_tokens(user_id);
CREATE INDEX idx_verification_tokens_token
  ON email_verification_tokens(token);
```

**Human:** Review schema
- Are relationships correct?
- Are indexes appropriate?
- Are constraints sufficient?
- Any missing fields?

**Deliverable:** Database migration files

### Step 3: Repository Layer

**AI:** Implement data access layer

```go
// internal/repository/user_repository.go

type UserRepository struct {
    db *sql.DB
}

func (r *UserRepository) UpdateProfile(
    ctx context.Context,
    userID int,
    params UpdateProfileParams,
) (*User, error) {
    query := `
        UPDATE users
        SET name = $1, bio = $2, avatar_url = $3, updated_at = NOW()
        WHERE id = $4
        RETURNING id, email, name, bio, avatar_url, created_at, updated_at
    `

    var user User
    err := r.db.QueryRowContext(
        ctx, query,
        params.Name, params.Bio, params.AvatarURL, userID,
    ).Scan(&user.ID, &user.Email, &user.Name, &user.Bio,
            &user.AvatarURL, &user.CreatedAt, &user.UpdatedAt)

    if err != nil {
        return nil, fmt.Errorf("failed to update profile: %w", err)
    }

    return &user, nil
}

func (r *UserRepository) UpdateEmail(
    ctx context.Context,
    userID int,
    newEmail string,
) error {
    // Check if email already exists
    var exists bool
    err := r.db.QueryRowContext(
        ctx,
        "SELECT EXISTS(SELECT 1 FROM users WHERE email = $1 AND id != $2)",
        newEmail, userID,
    ).Scan(&exists)

    if err != nil {
        return fmt.Errorf("failed to check email: %w", err)
    }

    if exists {
        return ErrEmailAlreadyExists
    }

    // Update email and mark as unverified
    _, err = r.db.ExecContext(
        ctx,
        `UPDATE users
         SET email = $1, email_verified = FALSE, updated_at = NOW()
         WHERE id = $2`,
        newEmail, userID,
    )

    return err
}
```

**Human:** Review repository
- Is error handling correct?
- Are transactions used where needed?
- Is SQL injection prevented?
- Are edge cases handled?

**Deliverable:** Repository implementation

### Step 4: API Endpoints

**AI:** Implement API handlers

```go
// internal/handlers/user_handlers.go

func (h *UserHandler) UpdateProfile(w http.ResponseWriter, r *http.Request) {
    // Get user ID from auth context
    userID := r.Context().Value("user_id").(int)

    // Parse request body
    var req UpdateProfileRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "Invalid request body")
        return
    }

    // Validate input
    if err := validateUpdateProfile(req); err != nil {
        respondError(w, http.StatusBadRequest, err.Error())
        return
    }

    // Update profile
    user, err := h.repo.UpdateProfile(r.Context(), userID, req)
    if err != nil {
        log.Printf("Failed to update profile: %v", err)
        respondError(w, http.StatusInternalServerError, "Failed to update profile")
        return
    }

    // If email changed, send verification
    if req.Email != "" && req.Email != user.Email {
        if err := h.sendEmailVerification(user.ID, req.Email); err != nil {
            log.Printf("Failed to send verification: %v", err)
            // Don't fail the request, just log
        }
    }

    respondJSON(w, http.StatusOK, user)
}
```

**Human:** Review API
- Does it match the specification?
- Are status codes correct?
- Is authorization checked?
- Are errors handled appropriately?

**Deliverable:** API implementation

### Step 5: API Tests (E2E + Unit)

**AI:** Write comprehensive E2E tests and unit tests for API

```javascript
// tests/e2e/api/user-profile.cy.js

describe('API: User Profile', () => {
  let authToken
  let userId

  before(() => {
    // Login to get auth token
    cy.request('POST', '/api/v1/auth/login', {
      email: 'test@example.com',
      password: 'TestPass123!'
    }).then((response) => {
      authToken = response.body.token
      userId = response.body.user.id
    })
  })

  describe('PUT /api/v1/users/:id', () => {
    it('updates user profile successfully', () => {
      cy.request({
        method: 'PUT',
        url: `/api/v1/users/${userId}`,
        headers: { Authorization: `Bearer ${authToken}` },
        body: {
          name: 'Updated Name',
          bio: 'This is my bio',
          avatar_url: 'https://example.com/avatar.jpg'
        }
      }).then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body.name).to.eq('Updated Name')
        expect(response.body.bio).to.eq('This is my bio')
      })
    })

    it('returns 400 for invalid email', () => {
      cy.request({
        method: 'PUT',
        url: `/api/v1/users/${userId}`,
        headers: { Authorization: `Bearer ${authToken}` },
        body: { email: 'invalid-email' },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(400)
        expect(response.body.error).to.include('Invalid email')
      })
    })

    it('returns 409 for duplicate email', () => {
      // Create second user with email
      // Try to update first user to same email
      // Verify 409 response
    })

    it('returns 401 without auth token', () => {
      cy.request({
        method: 'PUT',
        url: `/api/v1/users/${userId}`,
        body: { name: 'Test' },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(401)
      })
    })

    it('returns 403 when updating another user', () => {
      const otherUserId = userId + 1
      cy.request({
        method: 'PUT',
        url: `/api/v1/users/${otherUserId}`,
        headers: { Authorization: `Bearer ${authToken}` },
        body: { name: 'Test' },
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.eq(403)
      })
    })
  })
})
```

```go
// tests/unit/validators_test.go

func TestValidateEmail(t *testing.T) {
    tests := []struct {
        email string
        valid bool
    }{
        {"user@example.com", true},
        {"invalid.email", false},
        {"", false},
        {"no-at-sign.com", false},
    }

    for _, tt := range tests {
        result := validateEmail(tt.email)
        if result != tt.valid {
            t.Errorf("validateEmail(%s) = %v, want %v",
                tt.email, result, tt.valid)
        }
    }
}
```

**Human:** Review and run tests
- Do E2E tests cover all API scenarios?
- Do unit tests cover edge cases and validations?
- Do all tests pass?
- Is coverage threshold met (typically 70-90%)?
- Is test data managed correctly?

**Deliverable:** Passing E2E and unit tests for API with good coverage

### Step 6: Frontend Implementation

**AI:** Build React components

```javascript
// src/components/ProfileEditor.jsx

import { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { updateProfile } from '../api/users'

export function ProfileEditor() {
  const { user, setUser } = useAuth()
  const [formData, setFormData] = useState({
    name: user.name,
    email: user.email,
    bio: user.bio || '',
    avatarUrl: user.avatarUrl || ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const updatedUser = await updateProfile(user.id, formData)

      // Optimistic update
      setUser(updatedUser)
      setSuccess(true)

      if (formData.email !== user.email) {
        setError('Please check your email to verify your new address')
      }
    } catch (err) {
      setError(err.message || 'Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="profile-editor">
      <div className="form-group">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          data-test="name-input"
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          data-test="email-input"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="bio">Bio</label>
        <textarea
          id="bio"
          data-test="bio-input"
          value={formData.bio}
          onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
          rows={4}
        />
      </div>

      {error && (
        <div data-test="error-message" className="error">
          {error}
        </div>
      )}

      {success && (
        <div data-test="success-message" className="success">
          Profile updated successfully!
        </div>
      )}

      <button
        data-test="submit-button"
        type="submit"
        disabled={loading}
      >
        {loading ? 'Saving...' : 'Save Changes'}
      </button>
    </form>
  )
}
```

**Human:** Review UI implementation
- Does it match the mockup?
- Are loading states shown?
- Are errors handled gracefully?
- Is accessibility considered?

**Deliverable:** Frontend components

### Step 7: UI Tests (E2E + Unit)

**AI:** Write E2E tests and unit tests for UI

```javascript
// tests/e2e/ui/profile-editor.cy.js

describe('UI: Profile Editor', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'TestPass123!')
    cy.visit('/profile/edit')
  })

  it('displays current user data', () => {
    cy.get('[data-test="name-input"]')
      .should('have.value', 'Test User')
    cy.get('[data-test="email-input"]')
      .should('have.value', 'test@example.com')
  })

  it('updates profile successfully', () => {
    cy.get('[data-test="name-input"]')
      .clear()
      .type('Updated Name')

    cy.get('[data-test="bio-input"]')
      .type('This is my new bio')

    cy.get('[data-test="submit-button"]').click()

    cy.get('[data-test="success-message"]')
      .should('be.visible')
      .and('contain', 'Profile updated successfully')

    // Verify data persisted
    cy.reload()
    cy.get('[data-test="name-input"]')
      .should('have.value', 'Updated Name')
  })

  it('shows loading state during save', () => {
    cy.intercept('PUT', '/api/v1/users/*', (req) => {
      req.reply({ delay: 1000 })  // Delay response
    })

    cy.get('[data-test="submit-button"]').click()
    cy.get('[data-test="submit-button"]')
      .should('contain', 'Saving...')
      .and('be.disabled')
  })

  it('shows error for duplicate email', () => {
    cy.get('[data-test="email-input"]')
      .clear()
      .type('existing@example.com')

    cy.get('[data-test="submit-button"]').click()

    cy.get('[data-test="error-message"]')
      .should('be.visible')
      .and('contain', 'Email already registered')
  })

  it('shows error when network fails', () => {
    cy.intercept('PUT', '/api/v1/users/*', {
      statusCode: 500,
      body: { error: 'Server error' }
    })

    cy.get('[data-test="name-input"]')
      .clear()
      .type('New Name')

    cy.get('[data-test="submit-button"]').click()

    cy.get('[data-test="error-message"]')
      .should('be.visible')
  })
})
```

```javascript
// tests/unit/ProfileEditor.test.js

import { render, fireEvent } from '@testing-library/react'
import { ProfileEditor } from './ProfileEditor'

test('validates email format before submission', () => {
  const { getByLabelText, getByText } = render(<ProfileEditor />)

  fireEvent.change(getByLabelText('Email'), {
    target: { value: 'invalid-email' }
  })
  fireEvent.click(getByText('Save Changes'))

  expect(getByText('Please enter a valid email')).toBeInTheDocument()
})

test('disables submit button when loading', () => {
  const { getByText } = render(<ProfileEditor loading={true} />)

  expect(getByText('Saving...')).toBeDisabled()
})
```

**Human:** Review and run UI tests
- Do E2E tests cover all user interactions?
- Do unit tests cover form validation and component logic?
- Do all tests pass?
- Is coverage threshold met (typically 70-90%)?
- Are error scenarios covered?
- Do tests use stable selectors?

**Deliverable:** Passing E2E and unit tests for UI with good coverage

### Step 8: Documentation

**AI:** Update all documentation

```markdown
## API Documentation

### Update User Profile

Updates the authenticated user's profile information.

**Endpoint:** `PUT /api/v1/users/:id`

**Authentication:** Required (JWT token)

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "bio": "Software engineer",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

**Response 200:**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "bio": "Software engineer",
  "avatar_url": "https://example.com/avatar.jpg",
  "email_verified": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400` - Invalid input
- `401` - Not authenticated
- `403` - Cannot edit another user's profile
- `409` - Email already registered
- `500` - Server error

**Notes:**
- Changing email marks `email_verified` as false
- Verification email is sent to new email address
- User must verify email before it becomes active
```

**Human:** Review documentation
- Is it accurate?
- Is it complete?
- Are examples correct?
- Is it easy to understand?

**Deliverable:** Updated documentation

### Step 9: Code Review

**Human:** Comprehensive code review

**Review Checklist:**

**Security:**
- [ ] SQL injection prevented?
- [ ] XSS vulnerabilities addressed?
- [ ] Authorization checked?
- [ ] Sensitive data protected?

**Performance:**
- [ ] Queries optimized?
- [ ] Indexes appropriate?
- [ ] N+1 queries avoided?
- [ ] Caching considered?

**Code Quality:**
- [ ] Follows project conventions?
- [ ] Error handling complete?
- [ ] Logging appropriate?
- [ ] No code duplication?

**Testing:**
- [ ] All E2E tests pass?
- [ ] All unit tests pass?
- [ ] Coverage thresholds met (typically 70-90%)?
- [ ] Edge cases covered?
- [ ] Error scenarios tested?
- [ ] Test data cleaned up?

**Documentation:**
- [ ] API docs accurate?
- [ ] Code comments clear?
- [ ] README updated?
- [ ] CHANGELOG updated?

**Deliverable:** Approved code or requested changes

### Step 10: Deployment

**AI:** Execute deployment

```bash
# Pre-deployment checks
npm run lint
npm run test          # Run all tests (unit + E2E)
npm run test:coverage # Verify coverage thresholds
npm run build

# Run migrations
psql -d production -f migrations/003_user_profiles.up.sql

# Deploy backend
git checkout main
git pull
git merge feature/profile-editing
git push

# Deploy frontend
npm run build
rsync -avz dist/ production:/var/www/app/

# Verify deployment
curl https://api.example.com/health
curl https://example.com
```

**Human:** Verify deployment
- Is the feature live?
- Do smoke tests pass?
- Are there any errors in logs?
- Is monitoring showing normal metrics?

**Deliverable:** Feature deployed to production

## Summary

### AI Responsibilities (Execute 100%)
1. Design database schema
2. Implement repository layer
3. Build API endpoints
4. Write comprehensive E2E tests and unit tests for API
5. Create frontend components
6. Write UI E2E tests and unit tests
7. Update documentation
8. Execute deployment commands

### Human Responsibilities (Validate 100%)
1. Write specification
2. Review database schema
3. Review repository implementation
4. Review API implementation
5. Verify API tests pass and coverage meets threshold
6. Review frontend implementation
7. Verify UI tests pass and coverage meets threshold
8. Review documentation
9. Conduct code review
10. Verify deployment

### Key Success Factors

**Clear Handoffs:**
- AI completes a step fully
- Hands off to human for review
- Human approves or requests changes
- Clear criteria for approval

**Quality Gates:**
- All tests (E2E + unit) must pass before proceeding
- Coverage thresholds must be met
- Reviews must approve before merging
- Deployments must verify before closing

**Systematic Process:**
- Follow steps in order
- Don't skip steps
- Document decisions
- Track progress

---

**Prev:** [Testing Strategy](./06-testing-strategy.md) | **Next:** [Feature Workflow](./08-feature-workflow.md)

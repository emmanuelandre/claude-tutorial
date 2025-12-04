# Code Review Best Practices

How to effectively review code in AI-first development where AI generates code and humans validate.

## The Three-Layer Review Model

In AI-first development, code passes through three review layers:

```
┌─────────────────────────────────────────┐
│  Layer 1: Self-Review (Developer)       │
│  - Read what AI generated               │
│  - Check it matches requirements        │
│  - Verify tests pass                    │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  Layer 2: Automated Review (CI)         │
│  - Linting and formatting               │
│  - Test execution                       │
│  - Security scanning                    │
│  - Coverage thresholds                  │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  Layer 3: Peer Review (Team)            │
│  - Architecture alignment               │
│  - Business logic correctness           │
│  - Edge cases and error handling        │
│  - Knowledge sharing                    │
└─────────────────────────────────────────┘
```

## Layer 1: Self-Review

Before submitting any PR, the developer (human) must review AI-generated code.

### Self-Review Checklist

**Understanding:**
- [ ] I understand what every line does
- [ ] I can explain the logic to someone else
- [ ] The code matches the specification

**Correctness:**
- [ ] The code does what was requested
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs

**Quality:**
- [ ] Code follows project conventions
- [ ] No unnecessary complexity
- [ ] No hardcoded values that should be configurable
- [ ] Tests are meaningful (not just for coverage)

**Security:**
- [ ] No secrets in code
- [ ] Input is validated
- [ ] No SQL injection vulnerabilities
- [ ] Authentication/authorization is correct

### Common AI Code Issues to Catch

**1. Over-engineering:**
```go
// AI sometimes creates unnecessary abstractions
// ❌ Over-engineered
type UserServiceInterface interface {
    CreateUser(ctx context.Context, req CreateUserRequest) (*CreateUserResponse, error)
}

type UserServiceImpl struct {
    repo UserRepositoryInterface
}

func NewUserService(repo UserRepositoryInterface) UserServiceInterface {
    return &UserServiceImpl{repo: repo}
}

// ✅ Simpler when you only have one implementation
type UserService struct {
    repo *UserRepository
}

func NewUserService(repo *UserRepository) *UserService {
    return &UserService{repo: repo}
}
```

**2. Missing error context:**
```go
// ❌ AI might return bare errors
if err != nil {
    return err
}

// ✅ Add context
if err != nil {
    return fmt.Errorf("failed to create user: %w", err)
}
```

**3. Incomplete validation:**
```go
// ❌ AI might miss edge cases
func CreateUser(email string, password string) error {
    // Missing: email format validation
    // Missing: password strength validation
    // Missing: duplicate email check
}

// ✅ Complete validation
func CreateUser(email string, password string) error {
    if !isValidEmail(email) {
        return ErrInvalidEmail
    }
    if len(password) < 8 {
        return ErrWeakPassword
    }
    if exists, _ := userExists(email); exists {
        return ErrDuplicateEmail
    }
    // ...
}
```

**4. Hardcoded values:**
```go
// ❌ Hardcoded configuration
token, _ := jwt.Sign(claims, "my-secret-key")
time.Sleep(5 * time.Second)

// ✅ Configurable
token, _ := jwt.Sign(claims, config.JWTSecret)
time.Sleep(config.RetryDelay)
```

---

## Layer 2: Automated Review

Automated checks catch issues before human review.

### Essential Automated Checks

**Linting:**
```yaml
# .github/workflows/ci.yml
- name: Lint Go
  run: golangci-lint run

- name: Lint TypeScript
  run: npm run lint

- name: Lint Python
  run: ruff check .
```

**Formatting:**
```yaml
- name: Check formatting
  run: |
    go fmt ./...
    git diff --exit-code  # Fail if changes
```

**Tests:**
```yaml
- name: Run tests
  run: go test -race -coverprofile=coverage.out ./...

- name: Check coverage
  run: |
    coverage=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
    if (( $(echo "$coverage < 70" | bc -l) )); then
      echo "Coverage $coverage% is below 70% threshold"
      exit 1
    fi
```

**Security scanning:**
```yaml
- name: Security scan
  run: gosec ./...

- name: Dependency audit
  run: npm audit --audit-level=high
```

### Pre-commit Hooks

Run checks locally before pushing:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: go-fmt
        name: Go format
        entry: go fmt ./...
        language: system
        pass_filenames: false

      - id: go-test
        name: Go test
        entry: go test ./...
        language: system
        pass_filenames: false

      - id: go-vet
        name: Go vet
        entry: go vet ./...
        language: system
        pass_filenames: false
```

---

## Layer 3: Peer Review

Human review focuses on what automation can't catch.

### What Reviewers Should Check

**1. Architecture alignment:**
- Does this follow our established patterns?
- Is this the right place for this code?
- Does it fit with our overall design?

**2. Business logic:**
- Does this correctly implement the requirements?
- Are there business edge cases not covered?
- Is the behavior correct for all user types?

**3. Maintainability:**
- Will future developers understand this?
- Is there unnecessary complexity?
- Are there opportunities to reuse existing code?

**4. Performance implications:**
- Are there N+1 query issues?
- Is there unnecessary data loading?
- Could this become slow at scale?

### Review Comment Guidelines

**Be specific:**
```markdown
❌ "This could be better"
✅ "Consider using a map here instead of a slice for O(1) lookup"
```

**Explain why:**
```markdown
❌ "Don't use string concatenation in a loop"
✅ "String concatenation in a loop creates many allocations.
    Use strings.Builder for better performance."
```

**Suggest solutions:**
```markdown
❌ "This validation is incomplete"
✅ "This validation is missing the case where email is empty.
    Consider: `if email == "" { return ErrEmptyEmail }`"
```

**Distinguish severity:**
```markdown
🔴 BLOCKER: Security issue - user input not sanitized
🟡 SHOULD FIX: Performance issue - N+1 queries
🟢 SUGGESTION: Consider extracting this to a helper function
❓ QUESTION: Why did we choose this approach over X?
```

### PR Size Guidelines

| Size | Lines Changed | Review Time | Guidance |
|------|--------------|-------------|----------|
| XS | < 50 | 5-10 min | Quick review |
| S | 50-200 | 15-30 min | Standard review |
| M | 200-500 | 30-60 min | Detailed review |
| L | 500-1000 | 1-2 hours | Consider splitting |
| XL | > 1000 | Too long | Must split |

**Large PRs should be split by:**
- Layer (database, API, tests separately)
- Feature (one PR per sub-feature)
- Refactor vs. feature (separate PRs)

---

## AI-Generated Code Review Checklist

Use this checklist specifically for AI-generated code:

### Functionality
- [ ] Code implements the requested feature correctly
- [ ] All acceptance criteria are met
- [ ] Edge cases are handled (empty inputs, nulls, boundaries)
- [ ] Error messages are helpful and user-friendly

### Code Quality
- [ ] Code follows project style guidelines
- [ ] Variable names are descriptive and consistent
- [ ] No dead code or commented-out code
- [ ] Functions are focused and not too long (< 50 lines)
- [ ] No unnecessary abstractions

### Testing
- [ ] Tests exist and are meaningful
- [ ] Tests cover happy path and error cases
- [ ] Tests are not just achieving coverage numbers
- [ ] Test names describe what they test

### Security
- [ ] No hardcoded secrets or credentials
- [ ] User input is validated and sanitized
- [ ] SQL queries use parameterized statements
- [ ] Authentication is checked where needed
- [ ] Sensitive data is not logged

### Performance
- [ ] No obvious N+1 query problems
- [ ] Database queries are efficient (indexes used)
- [ ] No unnecessary memory allocations
- [ ] Pagination is used for large datasets

### Documentation
- [ ] Public APIs are documented
- [ ] Complex logic has explanatory comments
- [ ] README is updated if needed
- [ ] CHANGELOG is updated

---

## Review Workflow

### Standard PR Flow

```
1. Developer creates PR
   ↓
2. Automated checks run (CI)
   ↓ (pass)
3. Request review from team member
   ↓
4. Reviewer examines code
   ↓
5. Reviewer leaves comments
   ↓ (if changes needed)
6. Developer addresses feedback
   ↓ (loop until approved)
7. Reviewer approves
   ↓
8. Developer merges (squash)
```

### Review Response Time

| Priority | Response Time | Merge Time |
|----------|--------------|------------|
| Critical hotfix | < 1 hour | Same day |
| Normal feature | < 24 hours | 2-3 days |
| Refactoring | < 48 hours | 1 week |
| Documentation | < 48 hours | 1 week |

### Handling Review Feedback

**As the author:**
- Respond to all comments
- Don't take feedback personally
- Ask for clarification if unclear
- Mark resolved comments as resolved

**As the reviewer:**
- Be constructive, not critical
- Acknowledge good work
- Approve when ready, don't delay
- Follow up on your comments

---

## Reviewing AI-Generated Tests

Tests from AI need special attention:

### Watch for Weak Tests

```javascript
// ❌ Test that always passes
test('user is created', () => {
    const user = createUser('test@example.com');
    expect(user).toBeDefined();  // Too weak
});

// ✅ Test with meaningful assertions
test('user is created with correct properties', () => {
    const user = createUser('test@example.com', 'password123');
    expect(user.email).toBe('test@example.com');
    expect(user.passwordHash).not.toBe('password123');
    expect(user.createdAt).toBeInstanceOf(Date);
});
```

### Watch for Missing Error Tests

```javascript
// AI often forgets error cases
describe('createUser', () => {
    test('creates user successfully', () => { /* ... */ });

    // ❌ Missing error tests
    // ✅ Add these:
    test('rejects invalid email', () => { /* ... */ });
    test('rejects weak password', () => { /* ... */ });
    test('rejects duplicate email', () => { /* ... */ });
});
```

### Watch for Hardcoded Test Data

```javascript
// ❌ Hardcoded IDs that might conflict
test('gets user by id', async () => {
    const user = await getUserById(1);  // ID 1 might not exist
    expect(user).toBeDefined();
});

// ✅ Create test data
test('gets user by id', async () => {
    const created = await createUser('test@example.com');
    const user = await getUserById(created.id);
    expect(user.email).toBe('test@example.com');
});
```

---

## Code Review Tools

### GitHub Features

- **Required reviews:** Enforce minimum reviewers
- **Code owners:** Auto-assign relevant reviewers
- **Branch protection:** Require CI pass and reviews
- **Review comments:** Inline code discussions

### Additional Tools

| Tool | Purpose |
|------|---------|
| `danger` | Automated PR checks and comments |
| `reviewdog` | Post linter results as PR comments |
| `codecov` | Coverage tracking and PR comments |
| `sonarqube` | Code quality and security analysis |

---

## Summary

**Key Principles:**
- Three layers: Self, Automated, Peer
- AI code needs extra scrutiny
- Keep PRs small and focused
- Be constructive in feedback
- Reviewers catch what automation can't

**Self-Review First:**
Always review AI-generated code yourself before requesting peer review. You're responsible for understanding and vouching for the code.

---

**Prev:** [Documentation Writing](./13-documentation-writing.md) | **Next:** [Security Practices](./15-security.md)

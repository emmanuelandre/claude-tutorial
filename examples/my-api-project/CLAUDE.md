# CLAUDE.md - my-api-project

## Overview

Go REST API with JWT authentication and PostgreSQL database. This is a reference implementation for the Claude Code workshop.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │────▶│  Database   │
│             │     │   (Go)      │     │ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────▼─────┐ ┌─────▼─────┐
              │ Handlers  │ │ Middleware│
              └─────┬─────┘ └───────────┘
                    │
              ┌─────▼─────┐
              │Repository │
              └─────┬─────┘
                    │
              ┌─────▼─────┐
              │  Models   │
              └───────────┘
```

## Tech Stack

- **Language:** Go 1.21+
- **Framework:** gorilla/mux (routing)
- **Database:** PostgreSQL 16
- **Authentication:** JWT (golang-jwt/jwt)
- **Password Hashing:** bcrypt
- **Container:** Docker + Docker Compose

## Project Structure

```
my-api-project/
├── cmd/
│   └── server/
│       └── main.go           # Application entry point
├── internal/
│   ├── handlers/             # HTTP handlers
│   │   ├── auth.go           # Auth handlers (register, login, refresh)
│   │   └── user.go           # User handlers
│   ├── middleware/           # HTTP middleware
│   │   └── auth.go           # JWT authentication middleware
│   ├── models/               # Data models
│   │   └── user.go           # User model
│   └── repository/           # Database operations
│       └── user.go           # User repository
├── migrations/               # Database migrations
│   ├── 001_create_users.up.sql
│   └── 001_create_users.down.sql
├── tests/                    # Test files
│   ├── e2e/                  # E2E tests
│   └── unit/                 # Unit tests
├── docker-compose.yml
├── Dockerfile
├── go.mod
├── go.sum
└── CLAUDE.md
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login, returns JWT | No |
| POST | `/api/auth/refresh` | Refresh JWT token | Yes |
| POST | `/api/auth/logout` | Invalidate token | Yes |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/me` | Get current user | Yes |
| PUT | `/api/users/me` | Update current user | Yes |

### Request/Response Format

**Register Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Login Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_at": "2025-01-16T10:00:00Z"
}
```

**Error Response:**
```json
{
  "error": "invalid credentials",
  "code": "AUTH_INVALID_CREDENTIALS"
}
```

## Git Workflow

### Branch Naming
```
feature/   - New features (feature/user-auth)
fix/       - Bug fixes (fix/login-validation)
refactor/  - Code refactoring (refactor/repository-layer)
test/      - Test additions (test/auth-e2e)
docs/      - Documentation (docs/api-readme)
```

### Commit Messages

Use conventional commits:
```
feat(auth): add JWT token refresh endpoint
fix(user): validate email format on registration
test(auth): add E2E tests for login flow
docs(api): update endpoint documentation
```

### Pre-Commit Checklist

Before every commit, ensure:
- [ ] `go fmt ./...` - Code is formatted
- [ ] `go vet ./...` - No suspicious constructs
- [ ] `go test ./...` - All tests pass
- [ ] `go build ./...` - Code compiles
- [ ] Coverage meets minimum threshold (70%)

## Testing Strategy

### E2E Tests (Mandatory)
Test complete user journeys:
- Registration flow
- Login flow
- Protected endpoint access
- Token refresh
- Error scenarios

### Unit Tests (Mandatory)
Test business logic:
- Password hashing/verification
- JWT generation/validation
- Email validation
- Repository methods (with mocks)

### Coverage Targets
- Overall: 70% minimum
- Handlers: 80% minimum
- Repository: 70% minimum

### Running Tests
```bash
# All tests
go test ./...

# With coverage
go test -cover ./...

# E2E tests only
go test ./tests/e2e/...

# Unit tests only
go test ./tests/unit/...
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `JWT_SECRET` | Secret for JWT signing | Yes | - |
| `JWT_EXPIRY` | Token expiry duration | No | 24h |
| `PORT` | Server port | No | 8080 |
| `ENV` | Environment (dev/prod) | No | dev |

### Example .env
```bash
DATABASE_URL=postgres://user:pass@localhost:5432/myapi?sslmode=disable
JWT_SECRET=your-256-bit-secret-key-here
JWT_EXPIRY=24h
PORT=8080
ENV=dev
```

## Common Commands

```bash
# Development
go run cmd/server/main.go          # Start server
go build -o bin/server ./cmd/server # Build binary

# Database
psql -d myapi -f migrations/001_create_users.up.sql   # Run migration
psql -d myapi -f migrations/001_create_users.down.sql # Rollback

# Docker
docker-compose up -d               # Start all services
docker-compose down                # Stop all services
docker-compose logs -f api         # View API logs

# Testing
go test ./... -v                   # Verbose test output
go test -coverprofile=coverage.out ./...  # Generate coverage
go tool cover -html=coverage.out   # View coverage report
```

## Code Patterns

### Handler Pattern
```go
func (h *AuthHandler) Register(w http.ResponseWriter, r *http.Request) {
    var req RegisterRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "invalid request body")
        return
    }

    // Validate
    if err := validateEmail(req.Email); err != nil {
        respondError(w, http.StatusBadRequest, err.Error())
        return
    }

    // Process
    user, err := h.userRepo.Create(r.Context(), req.Email, req.Password)
    if err != nil {
        respondError(w, http.StatusInternalServerError, "failed to create user")
        return
    }

    respondJSON(w, http.StatusCreated, user)
}
```

### Repository Pattern
```go
type UserRepository interface {
    Create(ctx context.Context, email, password string) (*User, error)
    GetByEmail(ctx context.Context, email string) (*User, error)
    GetByID(ctx context.Context, id int) (*User, error)
    Update(ctx context.Context, user *User) error
}
```

## Security Considerations

- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens expire after 24 hours
- Rate limiting on auth endpoints (10 requests/minute)
- Input validation on all endpoints
- SQL injection prevented via parameterized queries
- CORS configured for allowed origins only

## Development Workflow

1. **Read the spec** - Understand what you're building
2. **Write migration** - Database schema first
3. **Implement repository** - Data access layer
4. **Build handlers** - HTTP endpoints
5. **Add middleware** - Authentication, logging
6. **Write tests** - E2E then unit
7. **Run pre-commit checks** - Format, lint, test
8. **Commit and push** - Small, focused commits

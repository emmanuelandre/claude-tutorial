# Project Name

Brief one-sentence description of what this project does.

## Philosophy & Team Structure

### Core Development Philosophy

**API-First Development**
- Specifications drive implementation
- Database schema → API contracts → UI components
- E2E tests validate complete user journeys
- Documentation generated from OpenAPI specs

**Micro-Teams of 2**
- Teams of 2 humans + Claude Code
- Redundancy without coordination overhead
- Each team owns end-to-end features
- Parallel development without bottlenecks

**Zero External Dependencies**
- Be your own QA engineer
- Be your own DevOps engineer
- Write comprehensive E2E tests yourself
- Deploy and monitor your own code
- Own the entire vertical slice

**Testing Philosophy**
- E2E tests are mandatory (API + UI user journeys)
- Unit tests are mandatory (business logic, utilities, edge cases)
- Component tests are good to have (use test containers where applicable)
- Coverage measurement is important (track unit, component, and E2E coverage)
- Coverage thresholds vary by project (higher is better)
- Test-first approach: Define coverage targets and build testing infrastructure before implementation
- Tests are your regression safety net

## Overview

[Detailed description of the project, its purpose, and key features]

Example:
"A microservices-based platform for [domain]. Users can [key capabilities]. The system provides [main features] with [technical highlights]."

## Architecture

```
Users → Load Balancer → Web Server (Nginx:80/443)
                           ↓
                    Frontend (React:3000)
                           ↓
                    API Gateway (Go:8080)
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                   ↓
   PostgreSQL         Service A          Service B
     (5432)            (8001)             (8002)
        ↓                  ↓                   ↓
   TimescaleDB        NATS Bus         Message Queue
   (Analytics)      (Messaging)
```

### Services

1. **api-service** (Go 1.21+) - Port 8080
   - Main REST API with OAuth 2.0 and JWT authentication
   - RBAC with user groups and permissions
   - PostgreSQL repository layer
   - Entry point: `cmd/api/main.go`
   - Structure: `internal/{handlers,middleware,models,repository}`
   - NATS publisher for async events

2. **worker-service** (Go 1.21+) - Port 8001
   - Background job processor
   - NATS subscriber for events
   - Processes async tasks
   - Entry point: `cmd/worker/main.go`

3. **ui-service** (React 18+) - Port 3000 (dev), 80/443 (prod)
   - Vite-based React app with React Router v6
   - OAuth login flow with JWT token management
   - Build output: `dist/` directory
   - WebSocket connection for real-time updates

4. **infra** - Infrastructure orchestration
   - Docker Compose, Nginx reverse proxy
   - PostgreSQL 15+, TimescaleDB (if using time-series data)
   - NATS messaging broker
   - Management scripts: `build-and-run.sh`, `stop.sh`, `logs.sh`

### Database

PostgreSQL with core tables:
- `users` - User accounts (OAuth)
- `user_groups` - Groups (admin, user, viewer)
- `permissions` - RBAC permissions (resource:action format)
- `audit_logs` - Comprehensive audit trail
- [Your domain-specific tables]

Migrations located in `api-service/migrations/`

### NATS Messaging

Event-driven architecture using NATS:

**Subjects:**
- `user.created` - New user registration
- `user.updated` - User profile changes
- `[resource].created` - Resource creation events
- `[resource].updated` - Resource update events
- `[resource].deleted` - Resource deletion events

**Publishers:**
- API service publishes events after database commits
- Events are fire-and-forget (async)

**Subscribers:**
- Worker service processes events
- Each service can subscribe to relevant subjects
- Handle failures with retry logic

## Tech Stack

### Backend
- **Language**: Go 1.21+
- **Framework**: Standard library + gorilla/mux
- **Database**: PostgreSQL 15+ (with TimescaleDB extension if needed)
- **ORM**: None - use database/sql directly or lightweight wrapper
- **Authentication**: JWT + OAuth 2.0 (Google, GitHub)
- **Messaging**: NATS 2.x
- **API Docs**: OpenAPI 3.0 + Swagger UI

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite 5.x
- **Router**: React Router v6
- **State**: Zustand (or Redux Toolkit)
- **Forms**: React Hook Form
- **UI**: Material-UI / Chakra UI / Tailwind CSS
- **HTTP**: Axios

### Testing
- **E2E Tests (Mandatory)**: Cypress 13.x for API and UI testing
- **Unit Tests (Mandatory)**: Go's testing package, Jest/Vitest for frontend
- **Component Tests (Good to have)**: Test containers (Testcontainers) for microservices integration
- **Coverage Tools**:
  - Unit: `jest --coverage`, `vitest --coverage`, `go test -coverprofile=coverage.out`
  - E2E: `@cypress/code-coverage` plugin with NYC
  - Merge: `nyc merge` to combine unit + E2E + component coverage
  - Thresholds: Typically 70-90% (varies by project criticality)

### DevOps
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **CI/CD**: GitHub Actions
- **Deployment**: Docker Swarm / Kubernetes / AWS ECS
- **Monitoring**: Prometheus + Grafana (optional)

## Development Workflow

### Git Workflow

**IMPORTANT - Repository Structure:**
- Parent directory is NOT a git repository (if using multi-repo setup)
- Each service subdirectory is its own independent git repository
- DO NOT initialize git in the root - keep it as a container

**Branch Naming Convention:**
```
<type>/<short-description>

Types:
- feature/  - New features or enhancements
- fix/      - Bug fixes
- refactor/ - Code refactoring without functionality changes
- docs/     - Documentation changes
- test/     - Test additions or modifications
- chore/    - Maintenance tasks (dependencies, tooling)
- perf/     - Performance improvements

Examples:
feature/user-authentication
fix/login-redirect-loop
refactor/extract-auth-middleware
docs/update-api-documentation
test/add-checkout-e2e-tests
```

**Commit Message Format:**

Follow **Conventional Commits** (https://www.conventionalcommits.org):

```
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, refactor, docs, style, test, chore, perf, ci, build
Scopes: api, ui, worker, infra, test

Examples:
feat(api): add user profile endpoint
fix(ui): resolve OAuth token refresh loop
refactor(api): extract validation middleware
docs: update deployment guide
test(api): add E2E tests for auth flow
```

**IMPORTANT COMMIT RULES:**
- ✅ Use conventional commits format
- ✅ Be concise and descriptive
- ❌ **DO NOT add "Co-Authored-By" or "Generated with Claude Code"**
- ❌ **DO NOT add emojis in commit messages**
- ✅ Keep commit message body optional unless complex change needs explanation

### Workflow Rules

1. **NEVER commit directly to main branch**
2. **NEVER merge branches to main** - only human merges via GitHub PR
3. Always create feature branch from main
4. **MANDATORY: Run lint and tests before EVERY commit** (see Pre-Commit Checks)
5. Push branch and open pull request
6. **Human reviews and merges PR** - AI does NOT merge
7. Delete branch after merge (done automatically by GitHub)

### Pre-Commit CI Checks

**CRITICAL REQUIREMENT: These checks MUST pass locally before committing. DO NOT commit if any check fails.**

**Workflow:**
1. Make code changes
2. Run all checks below for modified service(s)
3. Fix any failures
4. Only commit when ALL checks pass
5. If you commit code that fails CI, you have violated this requirement

#### Backend (Go) Checks

```bash
cd api-service

# 1. Format code
go fmt ./...

# 2. Run tests with coverage (aim for >= 40% for critical paths)
go test -v -race -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep total

# 3. Run linter (if golangci-lint installed)
golangci-lint run --timeout=5m

# 4. Build
go build ./...
```

#### Frontend (React) Checks

```bash
cd ui-service

# 1. Run ESLint
npm run lint

# 2. Build (must succeed)
npm run build
```

#### E2E Tests (Mandatory)

```bash
# Run all E2E tests before merging
npm run test:e2e:api    # API E2E tests
npm run test:e2e:ui     # UI E2E tests
```

### Git Workflow Example

```bash
# Create branch
git checkout main
git pull origin main
git checkout -b feature/your-feature

# Make changes...

# Run CI checks locally
cd api-service
go fmt ./...
go test -v -race -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep total
go build ./...

cd ../ui-service
npm run lint
npm run build

# Run E2E tests
npm run test:e2e

# Commit changes (only if ALL checks pass)
git add .
git commit -m "feat(api): add user profile endpoint"

# Push and create PR
git push origin feature/your-feature
gh pr create --title "feat: Add user profile endpoint" \
  --body "## Summary
- Implement GET/PUT /api/v1/users/:id
- Add E2E tests for profile operations
- Update OpenAPI spec

## Testing
- All E2E tests pass
- Manual testing completed"
```

## Project Structure

```
project-name/
├── api-service/              # Go API
│   ├── cmd/
│   │   └── api/
│   │       └── main.go       # Entry point
│   ├── internal/
│   │   ├── handlers/         # HTTP request handlers
│   │   ├── middleware/       # Auth, CORS, audit logging
│   │   ├── models/           # Data structures
│   │   ├── repository/       # Database access layer
│   │   └── nats/             # NATS publishers
│   ├── migrations/           # Database migrations
│   │   ├── 001_initial.up.sql
│   │   └── 001_initial.down.sql
│   ├── tests/
│   │   └── e2e/              # API E2E tests (Cypress)
│   ├── go.mod
│   └── go.sum
│
├── ui-service/               # React Frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components (routes)
│   │   ├── hooks/            # Custom React hooks
│   │   ├── store/            # State management
│   │   ├── api/              # API client functions
│   │   └── main.jsx          # Entry point
│   ├── public/               # Static assets
│   ├── tests/
│   │   └── e2e/              # UI E2E tests (Cypress)
│   └── package.json
│
├── worker-service/           # Background workers (Go)
│   ├── cmd/
│   │   └── worker/
│   │       └── main.go
│   ├── internal/
│   │   ├── handlers/         # Event handlers
│   │   └── nats/             # NATS subscribers
│   └── go.mod
│
├── infra/                    # Infrastructure
│   ├── docker/
│   │   ├── Dockerfile.api
│   │   ├── Dockerfile.ui
│   │   ├── Dockerfile.worker
│   │   └── docker-compose.yml
│   ├── nginx/
│   │   └── nginx.conf
│   ├── scripts/
│   │   ├── build-and-run.sh
│   │   ├── stop.sh
│   │   └── logs.sh
│   └── .env.example
│
├── docs/                     # Documentation
│   ├── api.md                # API documentation
│   ├── database.md           # Database schema
│   └── deployment.md         # Deployment guide
│
└── README.md                 # Project overview
```

## Common Commands

### Development

```bash
# Start all services (Docker)
cd infra && ./scripts/build-and-run.sh

# Stop all services
cd infra && ./scripts/stop.sh

# View logs
cd infra && ./scripts/logs.sh [service-name]

# Start API only (local development)
cd api-service && go run cmd/api/main.go

# Start UI only (local development)
cd ui-service && npm run dev
```

### Database

```bash
# Connect to PostgreSQL
docker exec -it postgres psql -U dbuser -d dbname

# Run migrations
cd api-service
psql -d dbname -f migrations/001_initial.up.sql

# Or use migration tool (e.g., golang-migrate)
migrate -path migrations -database "postgres://user:pass@localhost:5432/dbname" up
```

### Testing

```bash
# Run all tests (unit + E2E)
npm test

# Run unit tests only
npm run test:unit

# Run unit tests with coverage
npm run test:unit:coverage
# or for Go:
cd api-service && go test -coverprofile=coverage.out ./...
cd api-service && go tool cover -html=coverage.out

# Run E2E tests
npm run test:e2e

# Run E2E tests with coverage
npm run test:e2e:coverage

# Run API E2E tests only
cd api-service && npm run test:e2e

# Run UI E2E tests only
cd ui-service && npm run test:e2e

# Run in headed mode (see browser)
npm run test:e2e:headed

# Open Cypress UI
npx cypress open

# Generate combined coverage report (unit + E2E + component)
npm run coverage:merge
npx nyc report --reporter=html --reporter=text
open coverage/index.html

# Check coverage thresholds
npx nyc check-coverage --lines 80 --functions 80 --branches 80
```

### Code Quality

```bash
# Go formatting
go fmt ./...

# Go linting
golangci-lint run

# React linting
npm run lint

# Fix linting issues
npm run lint --fix
```

### Build and Deploy

```bash
# Build Go API
cd api-service && go build -o bin/api cmd/api/main.go

# Build React UI
cd ui-service && npm run build

# Build Docker images
cd infra && docker-compose build

# Deploy to production
cd infra && ./scripts/deploy.sh
```

## Key Architectural Patterns

### API Layer (Go)

**Route → Handler → Service → Repository Pattern**

```go
// internal/handlers/user_handler.go
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    userID := mux.Vars(r)["id"]

    // Call repository layer
    user, err := h.userRepo.FindByID(r.Context(), userID)
    if err != nil {
        respondError(w, http.StatusNotFound, "User not found")
        return
    }

    respondJSON(w, http.StatusOK, user)
}

// internal/repository/user_repository.go
func (r *UserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    var user User
    err := r.db.QueryRowContext(ctx,
        "SELECT id, email, name, created_at FROM users WHERE id = $1",
        id,
    ).Scan(&user.ID, &user.Email, &user.Name, &user.CreatedAt)

    if err == sql.ErrNoRows {
        return nil, ErrNotFound
    }
    return &user, err
}
```

**Handler → Repository (No Service Layer for Simple CRUD)**
- For simple CRUD operations, call repository directly from handlers
- Add service layer only when you have complex business logic

### NATS Event Publishing (Go)

```go
// internal/nats/publisher.go
type Publisher struct {
    nc *nats.Conn
}

func (p *Publisher) PublishUserCreated(user *User) error {
    data, _ := json.Marshal(user)
    return p.nc.Publish("user.created", data)
}

// In handler after successful database insert
func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    // ... create user in database
    user, err := h.userRepo.Create(ctx, userData)
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to create user")
        return
    }

    // Publish event (fire-and-forget)
    if err := h.nats.PublishUserCreated(user); err != nil {
        log.Printf("Failed to publish user.created event: %v", err)
        // Don't fail the request - event publishing is async
    }

    respondJSON(w, http.StatusCreated, user)
}
```

### NATS Event Subscription (Go)

```go
// cmd/worker/main.go
func main() {
    nc, _ := nats.Connect(nats.DefaultURL)

    // Subscribe to user.created events
    nc.Subscribe("user.created", func(m *nats.Msg) {
        var user User
        json.Unmarshal(m.Data, &user)

        // Process event
        sendWelcomeEmail(user)
        createDefaultSettings(user)
    })

    select {} // Keep running
}
```

### Frontend State Management (Zustand)

```javascript
// store/userStore.js
import { create } from 'zustand'

export const useUserStore = create((set) => ({
  user: null,
  loading: false,

  fetchUser: async (id) => {
    set({ loading: true })
    const user = await api.getUser(id)
    set({ user, loading: false })
  },

  updateUser: async (id, data) => {
    const updated = await api.updateUser(id, data)
    set({ user: updated })
  }
}))
```

### Authentication Flow

1. User clicks "Login with OAuth Provider" in UI
2. Redirects to `/api/v1/auth/google/login` (or GitHub, etc.)
3. OAuth callback at `/api/v1/auth/google/callback`
4. API creates/updates user in database
5. Returns JWT access token + refresh token to UI
6. UI stores tokens in localStorage
7. UI includes access token in Authorization header: `Bearer <token>`
8. API middleware validates JWT on protected routes
9. Token expires → UI calls `/api/v1/auth/refresh` with refresh token
10. API returns new access token

### Permission System

Permissions use `resource:action` format checked by middleware:

```go
// internal/middleware/permissions.go
func RequirePermission(permission string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            user := r.Context().Value("user").(*User)

            if !user.HasPermission(permission) {
                respondError(w, http.StatusForbidden, "Insufficient permissions")
                return
            }

            next.ServeHTTP(w, r)
        })
    }
}

// Usage in routes
router.Handle("/api/v1/users",
    authMiddleware(
        RequirePermission("users:read")(
            http.HandlerFunc(userHandler.ListUsers),
        ),
    ),
).Methods("GET")
```

**Common Permissions:**
- `users:read`, `users:create`, `users:update`, `users:delete`
- `[resource]:read`, `[resource]:create`, `[resource]:update`, `[resource]:delete`
- `admin:*` - Full administrative access

### Database Patterns

**All tables have standard timestamps:**
```sql
CREATE TABLE example (
    id SERIAL PRIMARY KEY,
    -- ... other columns ...
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP  -- Soft delete
);
```

**Soft Delete Pattern:**
- Never hard delete records (except for GDPR compliance)
- Set `deleted_at` timestamp instead
- Filter out deleted records in queries:
  ```sql
  SELECT * FROM users WHERE deleted_at IS NULL
  ```

**Use Transactions for Multi-Table Operations:**
```go
tx, _ := db.BeginTx(ctx, nil)
defer tx.Rollback()

// Multiple operations
_, err1 := tx.ExecContext(ctx, "INSERT INTO table1 ...")
_, err2 := tx.ExecContext(ctx, "INSERT INTO table2 ...")

if err1 != nil || err2 != nil {
    return err // Rollback happens automatically
}

tx.Commit()
```

## Environment Configuration

### API Service (.env)
```bash
# Required
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET=your-secret-key-here
NATS_URL=nats://localhost:4222

# OAuth (choose providers you use)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Optional
PORT=8080
ENV=development
LOG_LEVEL=debug
```

### UI Service (.env)
```bash
VITE_API_URL=http://localhost:8080
VITE_WS_URL=ws://localhost:8080
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

### Worker Service (.env)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
NATS_URL=nats://localhost:4222
```

## API Conventions

### RESTful Routes
```
GET    /api/v1/resources           # List all (with pagination)
POST   /api/v1/resources           # Create new
GET    /api/v1/resources/:id       # Get single
PUT    /api/v1/resources/:id       # Update (full replacement)
PATCH  /api/v1/resources/:id       # Partial update
DELETE /api/v1/resources/:id       # Delete (soft delete)

# Nested resources
GET    /api/v1/users/:id/orders    # Get user's orders
POST   /api/v1/users/:id/orders    # Create order for user
```

### Request/Response Format

**Authentication Header:**
```
Authorization: Bearer <jwt-token>
```

**Success Response:**
```json
{
  "data": { /* resource or array */ },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**Error Response:**
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "field": "email",
    "message": "Invalid email format"
  }
}
```

**Pagination:**
```
GET /api/v1/resources?page=1&limit=20&sort=created_at&order=desc
```

## Testing Strategy

### Test-First Approach with Comprehensive Coverage

**All tests are important for quality and confidence:**

- **E2E Tests (Mandatory)**: Test complete user journeys (API + UI)
- **Unit Tests (Mandatory)**: Test business logic, utilities, and edge cases
- **Component Tests (Good to have)**: Use test containers (Testcontainers) for microservices integration testing
- **Coverage Measurement**: Track coverage from unit, component, and E2E tests
- **Coverage Thresholds**: Vary by project, but higher is better (typically 70-90%)
- **Test-First Workflow**: Define coverage targets and build testing infrastructure/framework before implementation

### Setting Up Coverage Infrastructure

**Install Coverage Tools:**

```bash
# For JavaScript/TypeScript projects
npm install --save-dev @cypress/code-coverage nyc istanbul-lib-coverage babel-plugin-istanbul

# For unit tests
npm install --save-dev jest @jest/globals
# or
npm install --save-dev vitest @vitest/ui
```

**Configure package.json scripts:**

```json
{
  "scripts": {
    "test": "npm run test:unit && npm run test:e2e",
    "test:unit": "jest",
    "test:unit:coverage": "jest --coverage",
    "test:e2e": "cypress run",
    "test:e2e:coverage": "NODE_ENV=test cypress run",
    "coverage:merge": "npx nyc merge .nyc_output coverage/merged-coverage.json",
    "coverage:report": "npx nyc report --reporter=html --reporter=text"
  },
  "nyc": {
    "report-dir": "coverage",
    "reporter": ["html", "text", "lcov"],
    "exclude": ["**/*.test.js", "**/*.spec.js", "cypress/**"]
  }
}
```

**Configure Cypress for coverage (cypress.config.js):**

```javascript
const { defineConfig } = require('cypress')
const codeCoverageTask = require('@cypress/code-coverage/task')

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      codeCoverageTask(on, config)
      return config
    },
  },
})
```

**Add to cypress/support/e2e.js:**

```javascript
import '@cypress/code-coverage/support'
```

### API E2E Tests (Cypress)

```javascript
// tests/e2e/api/users.cy.js
describe('API: User Management', () => {
  let authToken

  before(() => {
    // Login to get auth token
    cy.request('POST', '/api/v1/auth/login', {
      email: 'test@example.com',
      password: 'TestPass123!'
    }).then((response) => {
      authToken = response.body.data.token
    })
  })

  it('creates a new user', () => {
    cy.request({
      method: 'POST',
      url: '/api/v1/users',
      headers: { Authorization: `Bearer ${authToken}` },
      body: {
        email: 'newuser@example.com',
        name: 'New User',
        role: 'user'
      }
    }).then((response) => {
      expect(response.status).to.eq(201)
      expect(response.body.data).to.have.property('id')
      expect(response.body.data.email).to.eq('newuser@example.com')
    })
  })

  it('returns 403 without permissions', () => {
    // Test with user without admin permissions
    cy.request({
      method: 'DELETE',
      url: '/api/v1/users/123',
      headers: { Authorization: `Bearer ${authToken}` },
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(403)
      expect(response.body.error).to.include('Insufficient permissions')
    })
  })
})
```

### UI E2E Tests (Cypress)

```javascript
// tests/e2e/ui/login.cy.js
describe('UI: User Login', () => {
  it('completes full login flow', () => {
    cy.visit('/login')

    cy.get('[data-test="email-input"]').type('test@example.com')
    cy.get('[data-test="password-input"]').type('TestPass123!')
    cy.get('[data-test="login-button"]').click()

    // Verify redirect to dashboard
    cy.url().should('include', '/dashboard')
    cy.contains('Welcome back').should('be.visible')

    // Verify token stored
    cy.window().then((win) => {
      expect(win.localStorage.getItem('accessToken')).to.exist
    })
  })

  it('shows error for invalid credentials', () => {
    cy.visit('/login')

    cy.get('[data-test="email-input"]').type('wrong@example.com')
    cy.get('[data-test="password-input"]').type('WrongPass123!')
    cy.get('[data-test="login-button"]').click()

    cy.get('[data-test="error-message"]')
      .should('be.visible')
      .and('contain', 'Invalid credentials')
  })
})
```

### Test Data Management

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.request({
    method: 'POST',
    url: '/api/v1/auth/login',
    body: { email, password }
  }).then((response) => {
    window.localStorage.setItem('accessToken', response.body.data.token)
  })
})

Cypress.Commands.add('createUser', (userData) => {
  return cy.request({
    method: 'POST',
    url: '/api/v1/users',
    headers: {
      Authorization: `Bearer ${Cypress.env('adminToken')}`
    },
    body: userData
  })
})

// Usage in tests
beforeEach(() => {
  cy.login('test@example.com', 'TestPass123!')
  cy.visit('/dashboard')
})
```

## Performance Considerations

### Backend (Go)
- Use connection pooling for database (`SetMaxOpenConns`, `SetMaxIdleConns`)
- Add database indexes on frequently queried columns
- Use pagination for list endpoints (max 100 items per page)
- Cache frequently accessed data in Redis (if needed)
- Profile slow endpoints: `import _ "net/http/pprof"`

### Frontend (React)
- Code splitting with `React.lazy()` and `Suspense`
- Lazy load routes
- Optimize images (WebP format, responsive sizes)
- Monitor bundle size (keep initial load < 500KB)
- Use React Query / SWR for API state caching

### Database
- Add indexes on foreign keys and frequently filtered columns
- Use `EXPLAIN ANALYZE` to identify slow queries
- Avoid N+1 queries (use JOINs or batch loading)
- Use database transactions for atomicity

## Security

### Backend Security
- Use prepared statements (prevents SQL injection)
- Validate all inputs
- Rate limiting (max requests per IP/user)
- CORS configured for specific origins only
- Helmet middleware for HTTP headers (if using framework)
- Password hashing with bcrypt (min 10 rounds)
- JWT tokens with expiration (15 min access, 7 days refresh)
- Secure cookies: HttpOnly, Secure, SameSite

### Frontend Security
- Sanitize user input before display
- Use Content Security Policy (CSP)
- No secrets in frontend code (use env variables)
- Validate all data from API
- Implement CSRF protection for state-changing operations

## Monitoring and Logging

### Logging Levels
- **ERROR**: Application errors, exceptions
- **WARN**: Potential issues, deprecated usage
- **INFO**: Important business events
- **DEBUG**: Detailed diagnostic information

### What to Log
- All API requests (method, path, status, duration, user ID)
- Authentication events (login, logout, token refresh, failures)
- Database query errors
- NATS publishing/subscription errors
- Performance metrics (slow queries, high memory usage)

### What NOT to Log
- Passwords or password hashes
- JWT tokens
- Credit card numbers
- API keys or secrets
- Any PII unless encrypted

### Structured Logging (Go)

```go
import "log/slog"

logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

logger.Info("User login",
    "user_id", userID,
    "email", email,
    "ip", r.RemoteAddr,
    "duration_ms", duration.Milliseconds(),
)
```

## Deployment

### Production Checklist
- [ ] All E2E tests passing
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] HTTPS enabled with valid certificate
- [ ] Rate limiting configured
- [ ] CORS configured for production domain
- [ ] Logging configured (centralized logs)
- [ ] Monitoring enabled (uptime, errors, performance)
- [ ] Backups configured (database, files)
- [ ] Security headers configured
- [ ] Load testing completed
- [ ] Disaster recovery plan documented

### Deployment Process
1. Create release branch from main
2. Run full test suite (E2E + load tests)
3. Build Docker images with version tags
4. Push images to container registry
5. Run database migrations on staging
6. Deploy to staging environment
7. Run smoke tests on staging
8. Deploy to production (blue-green or canary)
9. Monitor logs and metrics for 1 hour
10. Tag release in git (`v1.2.3`)

---

**Last Updated**: [Date]
**Maintained By**: [Team Name]
**Questions**: [Contact method or Slack channel]

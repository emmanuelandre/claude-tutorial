# Documentation Writing

How to write effective documentation for AI-first development projects.

## Why Documentation Writing Matters

In AI-first development, documentation serves as:
- **AI context** - Claude reads your docs to understand patterns
- **Team knowledge** - Shared understanding across developers
- **Decision history** - Why choices were made
- **Onboarding material** - New team members get up to speed

Good documentation is precise, scannable, and actionable.

## Types of Documentation

| Type | Purpose | Audience | Update Frequency |
|------|---------|----------|------------------|
| API Documentation | Endpoint contracts | Frontend devs, integrators | Per API change |
| Code Comments | Logic explanation | Future maintainers | With code changes |
| ADRs | Decision rationale | Team, future devs | Per major decision |
| README | Project entry point | All developers | Setup changes |
| Inline Types | Type contracts | All developers | With code changes |

---

## API Documentation

### OpenAPI/Swagger

For REST APIs, use OpenAPI specification:

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: User authentication and management API

paths:
  /api/auth/register:
    post:
      summary: Register a new user
      tags:
        - Authentication
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                  example: user@example.com
                password:
                  type: string
                  minLength: 8
                  example: securepassword123
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Invalid input
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '409':
          description: Email already exists

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
        created_at:
          type: string
          format: date-time
    Error:
      type: object
      properties:
        error:
          type: string
        code:
          type: string
```

### Markdown API Docs

For simpler projects, markdown tables work well:

```markdown
## POST /api/auth/register

Register a new user account.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| password | string | Yes | Min 8 characters |

### Response

**201 Created**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-01-15T10:00:00Z"
}
```

**400 Bad Request**
```json
{
  "error": "invalid email format",
  "code": "VALIDATION_ERROR"
}
```

### Example

```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```
```

### Best Practices for API Docs

**Do:**
- Include request and response examples
- Document all error codes
- Show authentication requirements
- Provide cURL examples
- Keep examples up-to-date

**Don't:**
- Document internal-only endpoints publicly
- Include sensitive data in examples
- Forget to update after API changes
- Use placeholder values without explaining

---

## Code Comments

### When to Comment

**Comment when:**
- Logic is non-obvious
- Business rules are embedded
- Workarounds exist for known issues
- Complex algorithms are used
- External dependencies have quirks

**Don't comment:**
- Obvious code (`i++ // increment i`)
- Self-explanatory function names
- Every line or function
- Commented-out code (delete it)

### Comment Patterns

**Function documentation (Go):**
```go
// CreateUser creates a new user with the given email and password.
// The password is hashed using bcrypt before storage.
// Returns ErrDuplicateEmail if the email already exists.
func (r *UserRepository) CreateUser(ctx context.Context, email, password string) (*User, error) {
    // ...
}
```

**Function documentation (TypeScript):**
```typescript
/**
 * Creates a new user with the given email and password.
 * @param email - User's email address (must be unique)
 * @param password - Plain text password (will be hashed)
 * @returns The created user object
 * @throws {DuplicateEmailError} If email already exists
 */
async function createUser(email: string, password: string): Promise<User> {
    // ...
}
```

**Inline comments for complex logic:**
```go
func calculateDiscount(order Order) float64 {
    discount := 0.0

    // Apply volume discount: 10% off for orders over $100
    if order.Total > 100 {
        discount += 0.10
    }

    // Loyalty discount: additional 5% for customers with 10+ orders
    // Note: This stacks with volume discount per business requirement #42
    if order.Customer.OrderCount >= 10 {
        discount += 0.05
    }

    // Cap total discount at 20% per finance policy
    if discount > 0.20 {
        discount = 0.20
    }

    return discount
}
```

**TODO comments:**
```go
// TODO(username): Implement retry logic for transient failures
// See: https://github.com/org/repo/issues/123

// FIXME: This query is slow for large datasets, needs optimization
// Tracked in JIRA-456

// HACK: Workaround for library bug, remove after upgrading to v2.0
// See: https://github.com/lib/issues/789
```

---

## Architecture Decision Records (ADRs)

ADRs document significant technical decisions and their rationale.

### ADR Template

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Date
2025-01-15

## Context
We need to choose a primary database for our application. The application
requires:
- ACID transactions for financial data
- JSON storage for flexible schemas
- Full-text search capabilities
- Horizontal read scaling

## Options Considered

### Option 1: PostgreSQL
**Pros:**
- ACID compliant
- Native JSON/JSONB support
- Full-text search built-in
- Read replicas for scaling
- Mature ecosystem

**Cons:**
- More complex than SQLite for small projects
- Requires separate server process

### Option 2: MongoDB
**Pros:**
- Flexible schema
- Built-in horizontal scaling
- Good for document-heavy workloads

**Cons:**
- No true ACID transactions (until v4.0)
- Different query paradigm
- Less mature tooling for our stack

### Option 3: MySQL
**Pros:**
- Widely used
- Good performance
- Simple replication

**Cons:**
- JSON support less mature than PostgreSQL
- Full-text search requires separate engine

## Decision
We will use **PostgreSQL** as our primary database.

## Rationale
PostgreSQL best meets our requirements:
1. ACID transactions are critical for financial data
2. JSONB allows flexible schemas without sacrificing query performance
3. Built-in full-text search avoids additional infrastructure
4. The team has PostgreSQL experience

## Consequences

### Positive
- Strong data integrity guarantees
- Single database handles JSON and relational data
- Proven scaling patterns available

### Negative
- Requires PostgreSQL expertise for optimization
- More operational overhead than SQLite
- Team needs to learn PostgreSQL-specific features

## Related
- ADR-002: Use TimescaleDB extension for time-series data
- ADR-003: Database backup and recovery strategy
```

### When to Write ADRs

Write an ADR when:
- Choosing between technologies (database, framework, library)
- Defining architectural patterns (microservices, monolith)
- Setting standards (API versioning, error handling)
- Making trade-offs (performance vs. simplicity)
- Changing existing patterns

### ADR File Organization

```
docs/
└── adr/
    ├── README.md           # Index of all ADRs
    ├── 001-database.md
    ├── 002-authentication.md
    ├── 003-api-versioning.md
    └── template.md         # ADR template
```

---

## Living Documentation

Documentation that stays in sync with code.

### Documentation as Code

**Generate docs from code:**
```bash
# Go - godoc
godoc -http=:6060

# TypeScript - TypeDoc
npx typedoc --out docs src/

# Python - Sphinx
sphinx-build -b html docs/ docs/_build/

# OpenAPI - Generate from annotations
swag init  # Go
```

**Test documentation examples:**
```go
// Example code in Go tests becomes documentation
func ExampleCreateUser() {
    user, err := CreateUser("test@example.com", "password123")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(user.Email)
    // Output: test@example.com
}
```

### Documentation Testing

Ensure documentation stays accurate:

```yaml
# GitHub Actions workflow
name: Docs
on: [push]
jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Test code examples in markdown
      - name: Test markdown code blocks
        run: npx markdown-doctest

      # Verify links aren't broken
      - name: Check links
        run: npx markdown-link-check **/*.md

      # Ensure OpenAPI spec is valid
      - name: Validate OpenAPI
        run: npx @redocly/cli lint openapi.yaml
```

### AI-Assisted Documentation Updates

Ask Claude to help maintain docs:

```
I've added a new endpoint POST /api/orders. Please:
1. Update the API documentation in docs/api.md
2. Add the endpoint to the OpenAPI spec
3. Create a code example for the README

Here's the handler code:
[paste code]
```

---

## README Best Practices

### Essential Sections

Every README should have:

1. **Title and description** - What is this?
2. **Quick start** - How to run it?
3. **Prerequisites** - What's needed?
4. **Installation** - Step-by-step setup
5. **Usage** - Basic examples
6. **Documentation links** - Where to learn more

### README vs Other Docs

| README | Other Docs |
|--------|------------|
| Quick start | Detailed guides |
| Overview | Deep dives |
| Basic examples | All examples |
| Setup steps | Troubleshooting |
| Links to more | Full content |

### Keep README Fresh

```markdown
<!-- In README.md -->
## Quick Start

<!-- IMPORTANT: Test these commands before each release -->
```bash
npm install
npm run dev
```

Last verified: 2025-01-15
```

---

## Documentation Style Guide

### Writing Style

**Be direct:**
```markdown
❌ "You might want to consider running the tests"
✅ "Run the tests"

❌ "It is recommended that users should..."
✅ "Users should..."
```

**Use active voice:**
```markdown
❌ "The configuration file is read by the server"
✅ "The server reads the configuration file"
```

**Be specific:**
```markdown
❌ "Set the timeout to an appropriate value"
✅ "Set the timeout to 30 seconds"
```

### Formatting Conventions

**Headings:**
- `#` for page title (one per doc)
- `##` for main sections
- `###` for subsections
- Don't skip levels

**Code blocks:**
- Always specify language
- Keep examples runnable
- Show expected output

**Lists:**
- Use bullets for unordered items
- Use numbers for sequences
- Keep items parallel in structure

---

## Prompting Claude for Documentation

### Generating API Docs
```
Generate OpenAPI 3.0 documentation for this Go handler:
[paste handler code]

Include:
- All request parameters
- All response codes
- Example requests and responses
- Authentication requirements
```

### Updating Documentation
```
The codebase has changed. Please update the documentation:

Changes made:
- Added rate limiting to /api/auth endpoints
- Changed password minimum from 6 to 8 characters
- Added new field 'phone' to user registration

Files to update:
- docs/api.md
- README.md
```

### Creating ADRs
```
I need to write an ADR for choosing between REST and GraphQL for our API.

Context:
- Team has REST experience
- Frontend needs flexible queries
- Performance is important

Please write a complete ADR evaluating both options.
```

---

**Prev:** [Documentation Organization](./12-documentation-organization.md) | **Next:** [Code Review](./14-code-review.md)

# The CLAUDE.md File

Your project's instruction manual for Claude Code.

## What is CLAUDE.md?

CLAUDE.md is a special file at your project root that tells Claude:
- What your project does
- How it's architected
- What conventions to follow
- How to work with your codebase

Think of it as **context that persists across all Claude sessions**.

## Why It's Essential

Without CLAUDE.md:
- ❌ Claude guesses your conventions
- ❌ Inconsistent code style
- ❌ Have to repeat context every session
- ❌ Violates project standards

With CLAUDE.md:
- ✅ Claude knows your standards
- ✅ Consistent code across features
- ✅ Context available immediately
- ✅ Follows your workflow automatically

## Basic Template

```markdown
# Project Name

## Overview
Brief description of what this project does.

## Architecture
High-level system design and components.

## Tech Stack
- Language/Framework
- Database
- Key libraries
- Infrastructure

## Development Workflow

### Git Workflow
- Branch naming conventions
- Commit message format
- PR process
- Review requirements

### Code Standards
- Linting rules
- Testing requirements
- Documentation requirements
- Pre-commit checks

## Project Structure
Directory layout and organization.

## Common Commands
Frequently used development commands.

## Key Patterns
Architectural patterns and conventions used.
```

## Complete Example

See the full example in [examples/claude-md-template.md](../examples/claude-md-template.md)

## Sections Explained

### 1. Project Overview
```markdown
## Overview
A REST API for managing tasks with user authentication,
real-time notifications, and PostgreSQL persistence.
```

Be specific about what the project does and its main features.

### 2. Architecture
```markdown
## Architecture
```
Users → API Gateway → Services → Database
                     ↓
                  Cache Layer
```
```

Visual diagrams help Claude understand system design.

### 3. Tech Stack
```markdown
## Tech Stack
- **Backend**: Node.js 18 + Express 4.x
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Testing**: Jest + Supertest
- **Deployment**: Docker + Kubernetes
```

Be specific about versions when relevant.

### 4. Git Workflow
```markdown
## Git Workflow

### Branch Naming
`<type>/<short-description>`

Types: feature, fix, refactor, docs, test

### Commit Format
`<type>(<scope>): <message>`

Examples:
- `feat(api): add user registration endpoint`
- `fix(auth): resolve token expiration bug`

### Rules
1. Never commit directly to main
2. All changes via PR
3. Run tests before commit
4. Lint must pass
```

Critical for maintaining code quality.

### 5. Code Standards
```markdown
## Code Standards

### Testing
- Unit tests for business logic
- E2E tests for API endpoints
- Minimum 70% coverage

### Before Commit
1. `npm run lint`
2. `npm test`
3. `npm run build`
```

Automated quality gates.

### 6. Project Structure
```markdown
## Project Structure
```
my-api/
├── src/
│   ├── controllers/  # HTTP handlers
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   └── middleware/   # Express middleware
├── tests/
│   ├── unit/
│   └── e2e/
└── docs/
```
```

Helps Claude navigate and organize code.

## Advanced Features

### Environment Variables
```markdown
## Environment Configuration
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string  
- `JWT_SECRET` - Token signing key
- `PORT` - Server port (default: 3000)
```

### API Patterns
```markdown
## API Conventions
- RESTful routes: `/api/v1/resources`
- JWT in Authorization header
- Error format: `{ error: string, details?: object }`
- Pagination: `?page=1&limit=20`
```

### Database Patterns
```markdown
## Database
- Migrations in `/migrations`
- Use transactions for multi-table operations
- Soft delete with `deleted_at` timestamp
- Created/updated timestamps on all tables
```

## Maintaining CLAUDE.md

### When to Update

✅ **Update when you:**
- Add new architectural components
- Change conventions or patterns
- Add new tools or libraries
- Modify development workflow
- Establish new best practices

❌ **Don't include:**
- Sensitive credentials
- Frequently changing details
- Implementation specifics
- Temporary notes

### Versioning

Keep CLAUDE.md in git:
```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with new API patterns"
```

## Tips for Effective CLAUDE.md

1. **Be Specific** - "Use Express 4.x" not "Use Express"
2. **Include Examples** - Show, don't just tell
3. **Keep It Current** - Update as project evolves
4. **Prioritize Important Info** - Most critical stuff first
5. **Use Clear Headings** - Easy to navigate
6. **Add Visual Diagrams** - Architecture, data flow, etc.

## Common Mistakes

❌ **Too Vague**
```markdown
## Tech Stack
- Node.js
- Database
```

✅ **Specific**
```markdown
## Tech Stack
- Node.js 18 + Express 4.18
- PostgreSQL 15 with Prisma ORM
- Redis 7 for caching
```

❌ **Too Long**
- 50+ pages of dense text
- Rarely updated
- Includes everything ever discussed

✅ **Right Size**
- 1-5 pages core content
- Updated frequently
- Links to detailed docs

## Example Projects

- [API Service](../examples/api-service-claude.md)
- [React App](../examples/react-app-claude.md)
- [Microservices](../examples/microservices-claude.md)

---

**Prev:** [Setup Guide](./03-setup-guide.md) | **Next:** [Prompt Engineering](./05-prompt-engineering.md)

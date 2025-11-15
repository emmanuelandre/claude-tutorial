# Project Name

Brief one-sentence description of what this project does.

## Overview

A more detailed description of the project, its purpose, and key features.

Example:
"A full-stack task management application with real-time collaboration features. Users can create, assign, and track tasks across teams with integrated notifications and analytics."

## Architecture

```
Users → Load Balancer → Web Server (Nginx)
                           ↓
                    Frontend (React)
                           ↓
                    API Gateway (Express)
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                   ↓
   PostgreSQL       Redis Cache       WebSocket Server
   (Primary DB)     (Sessions)        (Real-time)
        ↓
   TimescaleDB
   (Analytics)
```

## Tech Stack

### Backend
- **Language**: Node.js 18.x
- **Framework**: Express 4.18
- **Database**: PostgreSQL 15 + TimescaleDB
- **Cache**: Redis 7
- **ORM**: Prisma 5.x
- **Authentication**: JWT + OAuth 2.0 (Google)
- **Real-time**: Socket.io 4.x

### Frontend
- **Framework**: React 18.3
- **Build Tool**: Vite 5.x
- **Router**: React Router v6
- **State**: Zustand 4.x
- **Forms**: React Hook Form
- **UI**: Material-UI 5.x
- **HTTP**: Axios

### Testing
- **E2E**: Cypress 13.x
- **API Tests**: Cypress (API testing)
- **Unit Tests**: Jest (optional, only for complex algorithms)

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: AWS (ECS + RDS + ElastiCache)
- **Monitoring**: Sentry (errors) + CloudWatch (logs)

## Development Workflow

### Git Workflow

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
feature/task-assignment
fix/notification-timing
refactor/database-queries
docs/update-api-docs
test/add-dashboard-tests
```

**Commit Message Format:**

Follow Conventional Commits (https://www.conventionalcommits.org):

```
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, refactor, docs, style, test, chore, perf, ci, build
Scopes: api, ui, db, auth, tasks, notifications, analytics

Examples:
feat(tasks): add drag-and-drop task reordering
fix(api): resolve race condition in task updates
refactor(db): optimize task query performance
docs: update deployment instructions
test(tasks): add E2E tests for task creation
```

**IMPORTANT RULES:**
- ✅ Use conventional commits format
- ✅ Be concise and descriptive
- ❌ **DO NOT add "Co-Authored-By" or "Generated with Claude Code"**
- ❌ **DO NOT add emojis in commit messages**

### Workflow Steps

1. **NEVER commit directly to main branch**
2. Always create feature branch from main
3. **MANDATORY: Run pre-commit checks before EVERY commit** (see below)
4. Push branch and open pull request
5. **User reviews and merges PR** - AI does NOT merge
6. Delete branch after merge

### Pre-Commit CI Checks

**CRITICAL: These checks MUST pass locally before committing.**

```bash
# Backend checks
cd api
npm run lint          # ESLint must pass
npm test             # All tests must pass
npm run build        # Build must succeed

# Frontend checks
cd ui
npm run lint         # ESLint must pass
npm run build        # Vite build must succeed

# If any check fails, DO NOT commit
```

## Project Structure

```
project-name/
├── api/                      # Backend (Node.js + Express)
│   ├── src/
│   │   ├── controllers/      # HTTP request handlers
│   │   ├── services/         # Business logic
│   │   ├── models/           # Prisma models
│   │   ├── middleware/       # Express middleware (auth, CORS, etc)
│   │   ├── routes/           # API route definitions
│   │   ├── utils/            # Helper functions
│   │   └── index.js          # Entry point
│   ├── prisma/
│   │   ├── schema.prisma     # Database schema
│   │   └── migrations/       # Database migrations
│   ├── tests/
│   │   ├── e2e/              # E2E tests (Cypress)
│   │   └── unit/             # Unit tests (optional)
│   └── package.json
│
├── ui/                       # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components (routes)
│   │   ├── hooks/            # Custom React hooks
│   │   ├── store/            # Zustand stores
│   │   ├── api/              # API client functions
│   │   ├── utils/            # Helper functions
│   │   └── main.jsx          # Entry point
│   ├── public/               # Static assets
│   ├── tests/
│   │   └── e2e/              # E2E tests (Cypress)
│   └── package.json
│
├── docs/                     # Documentation
│   ├── api.md                # API endpoint documentation
│   ├── database.md           # Database schema docs
│   └── deployment.md         # Deployment guide
│
├── docker/                   # Docker configuration
│   ├── Dockerfile.api
│   ├── Dockerfile.ui
│   └── docker-compose.yml
│
├── .github/
│   └── workflows/
│       ├── test.yml          # CI tests
│       └── deploy.yml        # CD deployment
│
├── CLAUDE.md                 # This file
└── README.md                 # Project overview
```

## Common Commands

### Development

```bash
# Start all services (Docker)
docker-compose up -d

# Start backend only
cd api && npm run dev

# Start frontend only
cd ui && npm run dev

# View logs
docker-compose logs -f [service-name]
```

### Database

```bash
# Run migrations
cd api && npx prisma migrate dev

# Generate Prisma client
npx prisma generate

# Open Prisma Studio (GUI)
npx prisma studio

# Seed database
npm run db:seed

# Reset database (caution!)
npx prisma migrate reset
```

### Testing

```bash
# Run all E2E tests
npm run test:e2e

# Run API E2E tests only
cd api && npm run test:e2e

# Run UI E2E tests only
cd ui && npm run test:e2e

# Run tests in headed mode (see browser)
npm run test:e2e:headed

# Open Cypress UI
npx cypress open
```

### Code Quality

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint --fix

# Format code
npm run format

# Type check (TypeScript)
npm run type-check
```

### Build and Deploy

```bash
# Build backend
cd api && npm run build

# Build frontend
cd ui && npm run build

# Build Docker images
docker-compose build

# Deploy to production
npm run deploy
```

## Key Architectural Patterns

### API Layer

**Route → Controller → Service → Repository Pattern**

```javascript
// routes/tasks.js - Define routes
router.post('/tasks', authMiddleware, taskController.createTask)

// controllers/taskController.js - Handle HTTP
async function createTask(req, res) {
  const task = await taskService.create(req.body, req.user.id)
  res.status(201).json(task)
}

// services/taskService.js - Business logic
async function create(taskData, userId) {
  // Validation, business rules
  return taskRepository.create(taskData, userId)
}

// repositories/taskRepository.js - Database access
async function create(taskData, userId) {
  return prisma.task.create({ data: { ...taskData, userId } })
}
```

### Frontend Components

**Page → Container → Presentational Pattern**

```javascript
// pages/TasksPage.jsx - Route component
function TasksPage() {
  return <TasksContainer />
}

// containers/TasksContainer.jsx - Data fetching, state
function TasksContainer() {
  const tasks = useTasksStore(state => state.tasks)
  const createTask = useTasksStore(state => state.createTask)

  return <TasksList tasks={tasks} onCreateTask={createTask} />
}

// components/TasksList.jsx - Pure presentation
function TasksList({ tasks, onCreateTask }) {
  return (
    <div>
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
      <CreateTaskButton onClick={onCreateTask} />
    </div>
  )
}
```

### State Management (Zustand)

```javascript
// store/tasksStore.js
import { create } from 'zustand'

export const useTasksStore = create((set) => ({
  tasks: [],
  loading: false,

  fetchTasks: async () => {
    set({ loading: true })
    const tasks = await api.getTasks()
    set({ tasks, loading: false })
  },

  createTask: async (taskData) => {
    const task = await api.createTask(taskData)
    set(state => ({ tasks: [...state.tasks, task] }))
  }
}))
```

### Authentication Flow

1. User clicks "Login with Google"
2. Redirect to `/api/auth/google`
3. OAuth callback at `/api/auth/google/callback`
4. API creates/updates user in database
5. Returns JWT token + refresh token
6. UI stores tokens in localStorage
7. Include token in Authorization header for all requests
8. Middleware validates JWT on protected routes
9. Auto-refresh token when expired

### Database Patterns

- All tables have `created_at` and `updated_at` timestamps
- Soft delete using `deleted_at` timestamp (not hard delete)
- Use transactions for multi-table operations
- Migrations in `/prisma/migrations/`
- Use Prisma for all database access (no raw SQL unless necessary)

## Environment Configuration

### API (.env)
```bash
# Required
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional
PORT=8080
NODE_ENV=development
LOG_LEVEL=debug
```

### UI (.env)
```bash
VITE_API_URL=http://localhost:8080
VITE_WS_URL=ws://localhost:8080
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

## API Conventions

### RESTful Routes
```
GET    /api/v1/tasks           # List all tasks
POST   /api/v1/tasks           # Create task
GET    /api/v1/tasks/:id       # Get single task
PUT    /api/v1/tasks/:id       # Update task
DELETE /api/v1/tasks/:id       # Delete task

GET    /api/v1/tasks/:id/comments   # Nested resources
```

### Authentication
- JWT token in `Authorization: Bearer <token>` header
- Refresh token endpoint: `POST /api/v1/auth/refresh`
- Logout endpoint: `POST /api/v1/auth/logout`

### Error Response Format
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

### Success Response Format
```json
{
  "data": { /* resource */ },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Pagination
```
GET /api/v1/tasks?page=1&limit=20&sort=createdAt&order=desc
```

## Testing Strategy

**E2E Tests > Component Tests > Unit Tests**

### Priority 1: E2E Tests (Required)
- Test complete user journeys
- Test API endpoints with actual HTTP calls
- Test UI interactions with real browser
- Cover happy path + critical error scenarios
- MUST pass before merging

### Priority 2: Component Tests (Optional)
- Only for complex UI logic
- Form validation
- Multi-step wizards
- State machines

### Priority 3: Unit Tests (Rare)
- Only for critical algorithms
- Complex calculations
- Edge cases hard to test in E2E

### Test Coverage Requirements
- All API endpoints MUST have E2E tests
- All user-facing features MUST have UI E2E tests
- Unit test coverage is optional

## Performance Considerations

### Backend
- Use Redis caching for frequently accessed data
- Database indexes on frequently queried columns
- Pagination for list endpoints (max 100 items per page)
- Use database transactions for multi-table operations
- Monitor N+1 queries (use Prisma's query logging)

### Frontend
- Code splitting with React.lazy()
- Lazy load routes
- Optimize images (WebP format)
- Bundle size monitoring (max 500KB initial load)
- Use React Query for API state management

## Security

### Backend Security
- Helmet.js for HTTP headers
- CORS configured for specific origins only
- Rate limiting (max 100 requests/minute per IP)
- SQL injection prevention (use Prisma, no raw SQL)
- XSS prevention (sanitize inputs)
- CSRF tokens for state-changing operations
- Password hashing with bcrypt (min 10 rounds)

### Frontend Security
- Sanitize user input before display
- Use Content Security Policy
- HTTPOnly cookies for sensitive data
- No secrets in frontend code
- Validate all data from API

## Monitoring and Logging

### Logging Levels
- **ERROR**: Application errors, exceptions
- **WARN**: Potential issues, deprecated usage
- **INFO**: Important business events
- **DEBUG**: Detailed diagnostic information

### What to Log
- All API requests (method, path, status, duration)
- Authentication events (login, logout, failures)
- Database query errors
- External API failures
- Performance metrics (slow queries)

### What NOT to Log
- Passwords
- JWT tokens
- Credit card numbers
- Personal identification numbers
- Any PII (Personally Identifiable Information)

## Deployment

### Production Checklist
- [ ] All E2E tests passing
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] HTTPS enabled
- [ ] Monitoring configured
- [ ] Backups configured
- [ ] Error tracking enabled (Sentry)
- [ ] Performance monitoring enabled
- [ ] Security headers configured
- [ ] CORS configured for production domain

### Deployment Process
1. Create release branch from main
2. Run full test suite
3. Build Docker images
4. Push images to registry
5. Run database migrations
6. Deploy to staging
7. Run smoke tests
8. Deploy to production
9. Monitor logs and metrics
10. Tag release in git

## Support and Documentation

### Internal Docs
- `docs/api.md` - API endpoint documentation
- `docs/database.md` - Database schema and migrations
- `docs/deployment.md` - Deployment procedures
- `docs/troubleshooting.md` - Common issues and solutions

### External Resources
- [Project Wiki](https://github.com/org/repo/wiki)
- [Slack Channel](#team-channel)
- [Issue Tracker](https://github.com/org/repo/issues)

## Team Conventions

### Code Review Requirements
- At least 1 approval from team member
- All E2E tests must pass
- No linting errors
- Build succeeds
- Documentation updated if needed

### Working Hours and Communication
- Core hours: 9am-5pm (your timezone)
- Response time: Within 24 hours for PRs
- Use async communication (Slack, GitHub)
- Emergency contact: [method]

---

**Last Updated**: 2024-01-15
**Maintained By**: Development Team
**Questions**: #dev-team channel or create GitHub issue

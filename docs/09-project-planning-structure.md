# Project Planning & Documentation Structure

How to organize your project documentation for AI-first development.

## Philosophy

Centralized documentation enables:
- Context persistence across sessions
- Clear dependency mapping
- Systematic progress tracking
- Reusable specifications
- Knowledge sharing across team

## Recommended Structure

```
project-root/
├── service-api/              # Go API service (git repo)
├── service-ui/               # React UI service (git repo)
├── service-worker/           # Background workers (git repo)
├── infrastructure/           # Docker, Nginx, scripts (git repo)
│   └── project/              # CENTRAL DOCUMENTATION HUB
│       ├── planning/         # Master plans and schemas
│       ├── specs/            # Detailed feature specifications
│       ├── development/      # Workflow guides
│       ├── sessions/         # Session summaries
│       ├── archive/          # Historical context
│       └── infrastructure/   # Deployment docs
└── README.md
```

## The Documentation Hub

### Location
Create a central `project/` directory in your infrastructure repo (or dedicated docs repo).

**Why infrastructure repo?**
- Survives individual service changes
- Single source of truth
- Easy to reference from any service
- Natural home for cross-cutting concerns

### Directory Breakdown

#### 1. `/project/planning/`

Master planning documents that define the entire project.

**Files:**
```
planning/
├── devplan.md        # Master development plan
├── devprogress.md    # Progress tracker with checkboxes
├── database.md       # Complete database schema
└── sitemap.md        # Full UI sitemap with routes
```

**devplan.md** - Master Development Plan
```markdown
# Project Development Plan

## Development Strategy

### Core Principles
1. Database First - Schema before implementation
2. API First - Backend before frontend
3. Test Driven - Tests at each layer
4. Incremental - Follow dependency order
5. Vertical Slices - Complete stack per feature

### Implementation Workflow (Per Feature)
1. DATABASE: Migration → Repository → Mock data
2. BACKEND API: Handlers → Validation → Permissions
3. API E2E TESTS: Cypress API tests → All pass
4. FRONTEND UI: Components → Forms → Integration
5. UI E2E TESTS: Cypress UI tests → All pass
6. DOCUMENTATION: API docs → Comments → Changelog

### Dependency Map
```
Organizations → Users → Permissions → Features
Assets → Strategies → Backtests → Portfolios
```

### Development Phases
- Phase 0: Foundation (Auth, RBAC)
- Phase 1: Core Data (Assets, Prices)
- Phase 2: Strategies
- Phase 3: Backtesting
- ... (10 phases total)
```

**devprogress.md** - Progress Tracker
```markdown
# Development Progress

Last Updated: 2025-01-15

## Phase 0: Foundation ✅ COMPLETE

- [x] PostgreSQL database setup
- [x] User table and migration
- [x] Google OAuth integration
- [x] JWT authentication
- [x] User groups table
- [x] Permissions system
- [x] RBAC middleware
- [x] Audit logging
- [x] API E2E tests for auth
- [x] UI login flow

## Phase 1: Core Data 🔄 IN PROGRESS

- [x] Assets table and migration
- [x] Asset repository methods
- [x] API endpoints (CRUD)
- [x] API E2E tests
- [ ] Asset prices (TimescaleDB) ← NEXT
- [ ] Price ingestion worker
- [ ] UI asset management
- [ ] UI E2E tests

## Phase 2: Strategies 📋 PLANNED

- [ ] Strategies table
- [ ] Strategy repository
- [ ] API endpoints
- [ ] E2E tests
- [ ] UI strategy builder
...
```

**database.md** - Complete Database Schema
```markdown
# Database Schema

## Core Tables

### users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    avatar_url VARCHAR(500),
    group_id INTEGER REFERENCES user_groups(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_google_id ON users(google_id) WHERE deleted_at IS NULL;
```

### strategies
[Complete schema for all 26+ tables]
```

**sitemap.md** - Full UI Structure
```markdown
# UI Sitemap

## Public Routes
- `/` - Landing page
- `/login` - OAuth login
- `/about` - About page

## Protected Routes (Auth Required)

### Dashboard
- `/dashboard` - Main dashboard
  - Tables: users, strategies, backtests, portfolios
  - Permissions: None (all authenticated users)

### Strategies
- `/strategies` - Strategy list
  - Tables: strategies
  - Permissions: strategies:read

- `/strategies/new` - Create strategy
  - Tables: strategies, assets
  - Permissions: strategies:create

- `/strategies/:id` - Strategy details
  - Tables: strategies, strategy_assets, backtests
  - Permissions: strategies:read

### Admin
- `/admin/users` - User management
  - Tables: users, user_groups
  - Permissions: users:read, users:update
```

#### 2. `/project/specs/`

Detailed feature specifications with production-ready SQL, API contracts, and UI specs.

**Files:**
```
specs/
├── README.md                 # How to use specs
├── 00-sitemap-summary.md     # Quick reference
├── 01-auth-onboarding.md     # OAuth flow spec
├── 02-dashboard.md           # Dashboard spec
├── 03-strategies.md          # Strategy management
├── 04-assets.md              # Asset management
└── ... (one file per major feature)
```

**Example Spec Structure:**
```markdown
# Feature: Strategy Management

## Overview
Users can create, view, edit, and delete trading strategies.

## Database Schema

```sql
CREATE TABLE strategies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    config JSONB NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### List Strategies
**GET** `/api/v1/strategies`

**Query Parameters:**
- `page` (optional, default: 1)
- `limit` (optional, default: 20)

**Response 200:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Momentum Strategy",
      "description": "Buy on momentum indicators",
      "config": {...},
      "user_id": 1,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 42
  }
}
```

## UI Components

### StrategyList Component
**Location:** `src/pages/Strategies/StrategyList.jsx`

**Features:**
- Table with columns: Name, Description, Created
- Pagination controls
- Search/filter
- "New Strategy" button

**State Management:**
```javascript
const useStrategyStore = create((set) => ({
  strategies: [],
  loading: false,
  fetchStrategies: async () => {...}
}))
```

## E2E Tests

### API Tests
```javascript
describe('API: Strategies', () => {
  it('lists strategies with pagination', () => {
    cy.request('/api/v1/strategies?page=1&limit=10')
      .its('body.data')
      .should('have.length', 10)
  })
})
```

### UI Tests
```javascript
describe('UI: Strategy List', () => {
  it('displays strategies in table', () => {
    cy.visit('/strategies')
    cy.get('[data-test="strategy-row"]')
      .should('have.length.gt', 0)
  })
})
```
```

#### 3. `/project/development/`

Workflow guides and quick references for daily development.

**Files:**
```
development/
├── DEVELOPMENT.md       # Quick reference commands
└── CLAUDE_CONTEXT.md    # Detailed workflow for Claude
```

**DEVELOPMENT.md:**
```markdown
# Development Quick Reference

## Daily Workflow

### Start Development Session
```bash
cd infrastructure && ./build-and-run.sh
# Wait for all services to start
```

### Make Changes
1. Create feature branch
2. Implement (DB → API → Tests → UI)
3. Run pre-commit checks
4. Commit and push

### Pre-Commit Checks
```bash
# Go API
cd service-api
go fmt ./...
go test ./...
go build ./...

# React UI
cd service-ui
npm run lint
npm run build

# E2E Tests
npm run test:e2e
```

## Common Commands

### Database
```bash
# Connect
docker exec -it postgres psql -U dbuser -d dbname

# Run migration
psql -d dbname -f service-api/migrations/001_users.up.sql
```

### Docker
```bash
# Rebuild service
docker-compose build service-api
docker-compose up -d service-api

# View logs
docker logs service-api -f
```
```

**CLAUDE_CONTEXT.md:**
```markdown
# Claude Code Workflow Documentation

## Session Start Checklist

1. Verify CLAUDE.md is current
2. Check devprogress.md for current phase
3. Review relevant spec files
4. Create session notes file

## Feature Implementation Process

### Step 1: Review Specification
- Read spec file for the feature
- Understand database requirements
- Review API contracts
- Check UI mockups

### Step 2: Database Layer
Prompt:
```
"Implementing [feature] from specs/XX-feature.md.
Create PostgreSQL migration for [tables].
Follow our schema patterns from planning/database.md"
```

[Continue with all 10 steps...]

### Step 10: Document Session
Create file: `sessions/YYYY-MM-DD_feature-name.md`
```
# Session: Feature Name
Date: 2025-01-15
Duration: 3 hours
Branch: feature/feature-name

## Completed
- Database migration
- Repository implementation
- API endpoints
- E2E tests (12/12 passing)

## Next Steps
- UI components
- UI E2E tests
```
```

#### 4. `/project/sessions/`

Session summaries and progress notes.

**Format:**
```
sessions/
├── 2025-01-10_auth-implementation.md
├── 2025-01-12_strategy-crud.md
├── 2025-01-14_backtest-integration.md
└── 2025-01-15_dashboard-improvements.md
```

**Session Template:**
```markdown
# Session: [Feature/Task Name]

**Date:** 2025-01-15
**Duration:** 2.5 hours
**Branch:** feature/strategy-crud
**Status:** Completed

## Objectives
- Implement strategy CRUD operations
- Add E2E tests
- Create UI components

## Completed
- [x] Database migration (003_strategies.up.sql)
- [x] Go repository methods
- [x] API endpoints (GET, POST, PUT, DELETE)
- [x] API E2E tests (15 tests, all passing)
- [x] React components
- [x] UI E2E tests (8 tests, all passing)

## Challenges & Solutions
**Challenge:** Validation for strategy config JSONB field
**Solution:** Used Go json.RawMessage with custom validation

## Code Changes
- Files created: 12
- Files modified: 4
- Lines added: 847
- Tests added: 23

## Next Steps
- [ ] Implement strategy backtesting endpoint
- [ ] Add strategy optimization features
- [ ] Performance testing for large datasets

## References
- Spec: specs/03-strategies.md
- Commit: abc1234
- PR: #42
```

#### 5. `/project/archive/`

Historical context and obsolete documentation.

```
archive/
├── claude-history/          # Old session notes
├── obsolete/                # Deprecated docs
└── research/                # Investigation notes
```

#### 6. `/project/infrastructure/`

Deployment and ops documentation.

```
infrastructure/
├── deployment.md       # Deployment procedures
├── ci-cd-setup.md      # GitHub Actions config
└── monitoring.md       # Logging and monitoring
```

## Asking Claude to Use Your Structure

### Initial Prompt
```
"I have a comprehensive project documentation structure in
/infrastructure/project/ with:

- planning/devplan.md - Master development plan
- planning/devprogress.md - Progress tracker
- planning/database.md - Complete DB schema
- specs/ - 14 detailed feature specifications
- development/CLAUDE_CONTEXT.md - Workflow guide

Please read these files to understand:
1. Our development workflow (DB → API → Tests → UI)
2. Current phase and next tasks
3. Coding patterns and conventions

Then help me implement the next feature following our process."
```

### During Development
```
"Check planning/devprogress.md - what's our current phase?
What's the next uncompleted task?
Read the relevant spec file and let's implement it following
the 6-step workflow from planning/devplan.md"
```

### End of Session
```
"Create a session summary in project/sessions/ following
our template. Include:
- What we completed
- Challenges and solutions
- Code changes stats
- Next steps

Then update planning/devprogress.md to check off completed tasks."
```

## Benefits of This Structure

### For Solo Developers
- Track progress systematically
- Never lose context between sessions
- Reuse specifications across features
- Document decisions and rationale

### For Teams
- Single source of truth
- Onboard new developers quickly
- Parallel development without conflicts
- Knowledge preservation

### For AI Development
- Claude can read full context
- Specifications drive implementation
- Progress tracking is automatic
- Patterns are documented and reused

## Maintenance

### Weekly
- Update devprogress.md with completed tasks
- Create session summaries
- Review and update specs as needed

### Monthly
- Archive old session notes
- Update master plans
- Review and refactor documentation
- Assess what's working / not working

### Per Feature
- Create/update spec file
- Follow 6-step implementation workflow
- Document in session notes
- Update progress tracker

---

**Prev:** [Feature Workflow](./08-feature-workflow.md) | **Next:** [Scaling to Large Projects](./10-scaling-large-projects.md)

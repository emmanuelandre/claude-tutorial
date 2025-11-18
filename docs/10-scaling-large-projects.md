# Scaling to Large Projects

When building large, complex systems with Claude Code, proper project planning and progress tracking become essential. This guide shows you how to structure large projects for success using a phased approach with continuous monitoring and adjustment.

## The Challenge

Large projects present unique challenges:
- **100+ tasks** across multiple modules
- **Dependencies** between features that must be implemented in order
- **Multiple weeks** or months of development
- **Context loss** between sessions
- **Scope creep** and changing requirements
- **Progress tracking** to know what's done and what's next

## The Solution: Phased Development with Living Documentation

The key is creating a **project planning structure** that serves as both a roadmap and a progress tracker. This structure lives in your repository and evolves with your project.

### Core Components

```
your-project/
├── project/
│   ├── 00-CLAUDE.md              # Links to all planning docs
│   ├── planning/
│   │   ├── devplan.md            # Master plan with phases
│   │   ├── devprogress.md        # Active progress tracker
│   │   ├── database.md           # Complete DB schema
│   │   └── sitemap.md            # UI structure and routes
│   ├── specs/
│   │   ├── 01-feature-a.md       # Detailed spec for feature A
│   │   ├── 02-feature-b.md       # Detailed spec for feature B
│   │   └── ...
│   ├── sessions/
│   │   ├── 2025-01-15_session.md # What happened this session
│   │   └── ...
│   └── development/
│       ├── DEVELOPMENT.md        # Quick command reference
│       └── CLAUDE_CONTEXT.md     # Workflow documentation
```

## The Master Development Plan (devplan.md)

This is your project's blueprint. It breaks the entire project into manageable phases with clear dependencies.

### Structure

```markdown
# Project Development Plan

## Development Strategy

### Core Principles
1. **Database First**: Create schema before features
2. **API First**: Implement and test APIs before UI
3. **Test Driven**: Write tests before moving to next layer
4. **Incremental**: Build features in dependency order
5. **Vertical Slices**: Complete full stack for each feature

### Development Workflow (Per Feature)
```
DATABASE → BACKEND API → API TESTS → FRONTEND UI → UI TESTS → DOCS
```

## Dependency Map

Map out which features depend on others:

```
FOUNDATION
├── Organizations
├── Users → Organizations
├── User Groups → Organizations
├── Permissions → User Groups
└── Audit Logs

CORE DATA
├── Products
└── Product Prices → Products

FEATURES
├── Feature A → Users, Products
├── Feature B → Feature A
└── Feature C → Products
```

## Development Phases

Break your project into 10 phases (adjust based on size):

### Phase 0: Foundation (Week 1)

**Objective**: Set up database, authentication, and core infrastructure

#### Database Setup
- [ ] Create PostgreSQL database
- [ ] Set up migration system
- [ ] Create `organizations` table (Migration 001)
- [ ] Create `users` table (Migration 002)
- [ ] Create `user_groups` table (Migration 003)
- [ ] Create `permissions` table (Migration 004)
- [ ] Seed initial data

#### Authentication System
- [ ] Implement OAuth flow
- [ ] Implement JWT token generation
- [ ] Implement JWT middleware
- [ ] Implement permission checking middleware

#### Repository Layer
- [ ] Implement `OrganizationRepository`
- [ ] Implement `UserRepository`
- [ ] Implement `PermissionRepository`

#### API Endpoints
- [ ] `POST /api/v1/auth/login`
- [ ] `GET /api/v1/auth/callback`
- [ ] `GET /api/v1/users/me`

#### UI Pages
- [ ] Login page
- [ ] Registration page
- [ ] User profile page

#### Tests
- [ ] Test auth flow (OAuth + JWT)
- [ ] Test permissions middleware
- [ ] Test UI login flow

**Deliverable**: Working authentication system with RBAC

---

### Phase 1: Core Data (Week 2)

**Objective**: Implement core data models

[Similar detailed breakdown...]

---

### Phase 2-9: Feature Development

[Continue with feature-specific phases...]

---

### Phase 10: Polish & Production

**Objective**: Final polish and production deployment

[Final tasks...]
```

## The Progress Tracker (devprogress.md)

This is your **living status document**. Update it **every session** to track what's done and what's next.

### Structure

```markdown
# Project Development Progress

**Last Updated**: 2025-01-15 (Session 5)
**Current Phase**: Phase 2 - Products (84% Complete)
**Overall Progress**: 46% (131/286 tasks completed)

---

## Quick Stats

| Phase | Status | Progress | Tasks | Backend | UI | Tests |
|-------|--------|----------|-------|---------|----|----|
| Phase 0: Foundation | 🟢 Complete | 100% | 41/41 | 100% | 100% | 90% |
| Phase 1: Core Data | 🟢 Complete | 100% | 30/30 | 100% | 100% | 95% |
| Phase 2: Products | 🟡 In Progress | 84% | 21/25 | 90% | 30% | 85% |
| Phase 3: Orders | 🔴 Not Started | 0% | 0/28 | 0% | 0% | 0% |
| Phase 4: Inventory | 🔴 Not Started | 0% | 0/30 | 0% | 0% | 0% |

**Legend**: 🔴 Not Started | 🟡 In Progress | 🟢 Complete

---

## Current Sprint

**Sprint**: Phase 2 - Products - E2E API Tests & UI Pages
**Start Date**: 2025-01-15
**Focus**: Complete product management UI
**Status**: 🟡 In Progress

### Sprint Goals
1. ✅ Create comprehensive E2E API tests for products
2. ⏳ Build ProductForm.jsx page
3. ⏳ Build ProductDetail.jsx page
4. 🔜 Complete Phase 2 UI implementation

### Current Work
**Implementing Product Management UI**:
- Created ProductList.jsx with filtering and pagination
- Need to build create/edit form
- Need to build detail view

**Completed This Session**:
- ✅ Applied migrations 018, 019, 020
- ✅ Populated database with 15 sample products
- ✅ Created comprehensive API tests (70+ test cases)
- ✅ Updated API documentation

### Blockers
- ⏳ **Need UX mockups for product form** - using placeholder design
- ⏳ **Image upload functionality** - deferring to Phase 3

### Notes
- Phase 2 backend 90% complete (all API endpoints working)
- Phase 2 tests 85% complete (API tests done, UI tests TODO)
- Phase 2 UI 30% complete (list page only)
- Branch: `phase-2-products` (active)
```

## Session Notes (sessions/)

After each work session, create a brief summary documenting:
- What was accomplished
- Decisions made
- Blockers encountered
- Next steps
- Branches created or merged

### Example Session Note

```markdown
# Session: Phase 1 Completion

**Date**: 2025-01-14
**Duration**: 2 hours
**Phase**: Phase 1 - Core Data
**Status**: ✅ Complete

## Accomplishments

1. ✅ Created database migrations for products, prices, categories
2. ✅ Implemented repository layer with caching
3. ✅ Implemented API handlers and routes (10 endpoints)
4. ✅ Implemented UI pages (5 pages completed)
5. ✅ Wrote E2E tests (7 test files, 150+ test cases)

## Key Decisions

- **Decision**: Use TimescaleDB for price data (time-series optimization)
- **Rationale**: Price data grows rapidly, need efficient querying
- **Impact**: Added TimescaleDB extension to PostgreSQL

- **Decision**: Implement real-time price updates via WebSocket
- **Rationale**: Users need live price feeds
- **Impact**: Deferred to Phase 5 (out of scope for Phase 1)

## Blockers Resolved

- ~~PostgreSQL connection pooling issue~~ - Fixed by increasing max connections
- ~~CORS errors in development~~ - Added middleware configuration

## Next Steps

1. Merge `phase-1-core-data` branch to main
2. Update devprogress.md to mark Phase 1 complete
3. Begin Phase 2 planning
4. Create Phase 2 branch

## Branches

- Created: `phase-1-core-data`
- Status: Ready for PR
- Commits: 15 commits
- Tests: All passing ✅
```

## Feature Specifications (specs/)

For complex features, create detailed specification files with:
- User stories
- Database schema
- API endpoints (with request/response examples)
- UI mockups or descriptions
- Acceptance criteria

### Example Spec Structure

```markdown
# Feature Spec: Product Management

## Overview
Users can create, view, edit, and delete products with pricing, categories, and inventory tracking.

## User Stories

**As a seller**, I want to add products to my catalog so customers can purchase them.

**As a seller**, I want to organize products into categories so customers can browse easily.

## Database Schema

### products table
```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  org_id INTEGER NOT NULL REFERENCES organizations(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  category_id INTEGER REFERENCES categories(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### GET /api/v1/products
List all products with filtering and pagination

**Request:**
```http
GET /api/v1/products?category_id=5&page=1&limit=20
```

**Response:**
```json
{
  "products": [...],
  "total": 100,
  "page": 1,
  "limit": 20
}
```

### POST /api/v1/products
Create new product

**Request:**
```json
{
  "name": "Widget Pro",
  "description": "Advanced widget",
  "price": 29.99,
  "category_id": 5
}
```

**Response:**
```json
{
  "id": 123,
  "name": "Widget Pro",
  ...
}
```

[Continue with all endpoints...]

## UI Pages

### Product List Page (`/products`)
- Table view with columns: Name, Price, Category, Actions
- Filters: Category, Price range, Search
- Pagination: 20 per page
- Actions: View, Edit, Delete

### Product Form Page (`/products/new`, `/products/:id/edit`)
- Fields: Name, Description, Price, Category, Images
- Validation: Required fields, price format
- Save/Cancel buttons

[Continue with all pages...]

## Acceptance Criteria

- [ ] Users can create products with all required fields
- [ ] Products appear in list immediately after creation
- [ ] Users can filter by category
- [ ] Users can search by name
- [ ] Pagination works correctly
- [ ] Edit updates product in database
- [ ] Delete removes product (soft delete)
- [ ] All E2E tests pass
```

## CLAUDE.md Integration

Update your `CLAUDE.md` to reference the planning structure:

```markdown
## Development Documentation

All planning and specification documents are centralized in `project/`:

### Planning & Progress (`project/planning/`)
- **`devplan.md`**: Master development plan with 10 phases
- **`devprogress.md`**: Active progress tracker - update daily
- **`database.md`**: Complete database schema
- **`sitemap.md`**: Full UI sitemap

### Development Guides (`project/development/`)
- **`DEVELOPMENT.md`**: Quick reference guide
- **`CLAUDE_CONTEXT.md`**: Workflow documentation

### Feature Specs (`project/specs/`)
- `01-auth.md` - Authentication and authorization
- `02-products.md` - Product management
- `03-orders.md` - Order processing
[... etc ...]

### Work Sessions (`project/sessions/`)
Recent development session summaries

### Implementation Workflow (Per Feature)
```
1. DATABASE: Migration → Repository → Mock data
2. BACKEND API: Endpoints → Validation → Permissions
3. API E2E TESTS: Write → Run → Fix
4. FRONTEND UI: Components → Forms → Integration
5. UI E2E TESTS: Write → Run → Fix
6. DOCUMENTATION: Update docs → Comments
```

### Phase Order (Follow Dependencies)
```
Phase 0: Foundation (Auth, Users, Permissions) ← START HERE
Phase 1: Core Data Management
Phase 2: Primary Features
Phase 3: Secondary Features
...
Phase 10: Polish & Production
```
```

## Best Practices

### 1. Update Progress After Every Session

**DO THIS:**
```bash
# At end of session
1. Update devprogress.md with checkboxes
2. Create session note in sessions/
3. Update current phase percentage
4. Document blockers
5. Commit and push
```

### 2. Keep devplan.md Stable, devprogress.md Dynamic

- **devplan.md** = The original plan (rarely changes)
- **devprogress.md** = Current reality (updates every session)
- If plans change significantly, update devplan.md and note why

### 3. Use Checkboxes for Tracking

```markdown
- [x] Completed task
- [ ] Pending task
- [⏳] In progress task
- [🔜] Upcoming task
```

### 4. Track Percentages Accurately

Calculate percentages based on actual task completion:
```
Phase Progress = (Completed Tasks / Total Tasks) × 100
Overall Progress = (All Completed Tasks / All Total Tasks) × 100
```

### 5. Document Decisions

When you make important architectural or design decisions:
- Add to session notes
- Update relevant spec files
- Note the rationale

### 6. Adjust Plans When Reality Diverges

If you discover:
- A phase is 70% done but devprogress shows 0%
- New dependencies you didn't anticipate
- Features that should be split or combined

**Update the plan immediately** to reflect reality.

## Interactive Exercise: Multi-Phase Project

Let's practice building a multi-phase project from scratch.

### Exercise Overview

You'll create a **Task Management System** with:
- User authentication
- Projects and tasks
- Comments and attachments
- Dashboard with analytics

This will be broken into 4 phases (workshop will complete Phases 0-1).

### Phase 0: Foundation Setup

Create the planning structure and implement basic auth.

**Step 1: Initialize Project Structure**

Create the directory structure:
```bash
mkdir task-manager
cd task-manager
git init

mkdir -p project/{planning,specs,sessions,development}
mkdir -p api
mkdir -p ui
```

**Step 2: Create Master Plan**

**PROMPT:**
```
Create a file at project/planning/devplan.md for a Task Management System.

The system needs:
- User authentication (Google OAuth + JWT)
- Organizations and teams
- Projects (with members)
- Tasks (with assignees, due dates, priorities)
- Comments on tasks
- File attachments

Break this into 4 phases:
- Phase 0: Foundation (Auth, Users, Organizations)
- Phase 1: Projects (Project CRUD, Members)
- Phase 2: Tasks (Task CRUD, Comments, Attachments)
- Phase 3: Dashboard (Analytics, Reports)

For each phase, list:
- Database tables needed
- Repository layer functions
- API endpoints
- UI pages
- Tests

Follow the vertical slice workflow: DB → API → API Tests → UI → UI Tests

Use checkboxes for all tasks.
```

**Expected Result:**
Complete `devplan.md` with 4 phases, ~80-100 tasks total, dependency mapping.

---

**Step 3: Create Progress Tracker**

**PROMPT:**
```
Create project/planning/devprogress.md based on devplan.md.

Add:
- Quick Stats table showing all 4 phases
- Current Sprint section (Phase 0 - Foundation)
- Sprint Goals (5-7 goals for Phase 0)
- All Phase 0 tasks with checkboxes
- Status indicators: 🔴 Not Started | 🟡 In Progress | 🟢 Complete

Set Phase 0 to "🟡 In Progress" with 0% progress initially.
Mark all other phases as "🔴 Not Started".
```

**Expected Result:**
`devprogress.md` showing Phase 0 in progress, all tasks unchecked.

---

**Step 4: Create Database Schema Document**

**PROMPT:**
```
Create project/planning/database.md with complete schema for all 4 phases.

Include tables:
- organizations
- users
- user_groups
- permissions
- projects
- project_members
- tasks
- comments
- attachments

For each table:
- Column definitions with types
- Primary and foreign keys
- Indexes
- Constraints
- Comments explaining purpose

Use PostgreSQL syntax.
```

**Expected Result:**
Complete database schema document with all tables defined.

---

**Step 5: Implement Phase 0 - Database**

**PROMPT:**
```
Let's start Phase 0 implementation. I'm in the api/ directory.

Initialize a Go project:
- Create go.mod for "task-manager-api"
- Create directory structure: cmd/api, internal/{handlers,middleware,models,repository}, migrations/
- Create migrations for Phase 0 tables: organizations, users, user_groups, permissions

Generate migration files:
migrations/001_create_organizations.up.sql
migrations/002_create_users.up.sql
migrations/003_create_user_groups.up.sql
migrations/004_create_permissions.up.sql

Include seed data for:
- Default organization
- Admin user group
- Basic permissions (users:read, users:write, projects:read, projects:write, tasks:read, tasks:write)
```

**Expected Result:**
Go project initialized, 4 migration files created with seed data.

---

**Step 6: Mark Database Tasks Complete**

**PROMPT:**
```
Update project/planning/devprogress.md:
- Mark database setup tasks as complete [x]
- Update Phase 0 percentage based on completed tasks
- Update "Current Work" section
- Add to "Completed This Session" list
```

**Expected Result:**
Progress tracker shows ~20-30% Phase 0 complete.

---

**Step 7: Implement Phase 0 - Authentication**

**PROMPT:**
```
Implement Google OAuth + JWT authentication:

1. Create internal/models/user.go with User struct
2. Create internal/repository/user_repository.go with:
   - GetByID
   - GetByEmail
   - Create
   - Update
3. Create internal/handlers/auth_handler.go with:
   - GoogleLoginHandler
   - GoogleCallbackHandler
   - GetMeHandler
4. Create internal/middleware/auth.go with JWT validation
5. Create cmd/api/main.go with routes

Use these dependencies:
- github.com/gorilla/mux (routing)
- github.com/golang-jwt/jwt/v5 (JWT)
- github.com/lib/pq (PostgreSQL)
- golang.org/x/oauth2/google (OAuth)

Follow repository pattern - handlers never touch database directly.
```

**Expected Result:**
Auth system implemented with OAuth flow and JWT middleware.

---

**Step 8: Update Progress After Auth**

**PROMPT:**
```
Update project/planning/devprogress.md:
- Mark auth system tasks complete [x]
- Mark repository layer tasks complete [x]
- Mark API endpoint tasks complete [x]
- Update Phase 0 percentage
- Update "Completed This Session"
```

**Expected Result:**
Progress tracker shows ~60-70% Phase 0 complete.

---

### Phase 1: Projects (Out of Workshop Scope - Demo Only)

This phase demonstrates how to continue the workflow. **Not for workshop implementation** - instructor shows the process.

**Step 9: Begin Phase 1 - Database** (Instructor Demo)

**PROMPT:**
```
Starting Phase 1 - Projects.

First, update devprogress.md:
- Mark Phase 0 as 🟢 Complete (100%)
- Mark Phase 1 as 🟡 In Progress (0%)
- Update "Current Sprint" section to Phase 1
- Update "Sprint Goals" with Phase 1 goals

Then create migrations:
migrations/005_create_projects.up.sql
migrations/006_create_project_members.up.sql

Include:
- projects table (name, description, org_id, owner_id, created_at)
- project_members table (project_id, user_id, role)
- Indexes on foreign keys
- Seed data (2 sample projects)
```

**Expected Result:**
devprogress.md updated, Phase 1 started, migrations created.

---

**Step 10: Create Session Note** (Instructor Demo)

**PROMPT:**
```
Create project/sessions/2025-01-15_phase-0-completion.md:

Document:
- Session date and duration
- Phase completed: Phase 0 - Foundation
- What was accomplished (4 migrations, auth system, 3 repositories, 3 API endpoints)
- Decisions made (using Google OAuth, JWT tokens, gorilla/mux router)
- Next steps (Phase 1 - Projects database setup)
- Branches created (if any)

Use the session note format from the documentation.
```

**Expected Result:**
Session note created documenting Phase 0 completion.

---

### Phase 2-3: Tasks and Dashboard (Out of Workshop Scope)

These phases are included in the master plan but not implemented in the workshop. They demonstrate how the project continues beyond the workshop.

**Instructor shows:**
- How devprogress.md would be updated for Phase 2
- How spec files would guide implementation
- How session notes track decisions across weeks
- How percentages track overall project health

---

## Key Takeaways

### For Small Projects (< 20 tasks)
- Simple `CLAUDE.md` is enough
- No need for separate planning structure

### For Medium Projects (20-50 tasks)
- Create `project/devplan.md` with phases
- Update progress after each session

### For Large Projects (50+ tasks)
- Full planning structure with all components
- Daily updates to devprogress.md
- Session notes after every session
- Detailed specs for complex features

### Universal Best Practices
1. **Plan before coding** - Define all phases upfront
2. **Track religiously** - Update progress every session
3. **Document decisions** - Capture rationale in session notes
4. **Adjust when needed** - Update plan when reality diverges
5. **Use checkboxes** - Visual progress is motivating
6. **Calculate percentages** - Know where you stand

## Common Pitfalls

❌ **Don't:**
- Create planning docs then never update them
- Let devprogress.md drift from reality
- Skip session notes to "save time"
- Ignore dependencies and jump around phases
- Leave blockers undocumented

✅ **Do:**
- Update progress immediately after completing tasks
- Reassess plan every 5-10 sessions
- Document blockers and how you resolved them
- Follow dependency order strictly
- Celebrate phase completions

---

**Prev:** [Project Planning & Documentation Structure](./09-project-planning-structure.md)
**Next:** [Git Workflow](./11-git-workflow.md)

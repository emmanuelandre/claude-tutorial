# Claude Code Tutorial - Workshop Prompts

Copy and paste these prompts during the workshop exercises.

---

## Page 9: Create Your First Project

**PROMPT:**
```
mkdir my-api-project
cd my-api-project
git init

# Now ask Claude:
Help me create a CLAUDE.md file for a Go API project with:
- PostgreSQL database
- JWT authentication
- RESTful endpoints
- Docker deployment

Include project structure, git workflow, and testing strategy.
```

**EXPECTED RESULT:**
Claude creates a comprehensive CLAUDE.md with architecture, commands, and conventions

---

## Page 10: Initialize Git Workflow

**PROMPT:**
```
Create feature branch and set up git workflow:
- Branch naming convention: feature/initial-setup
- Conventional commits enabled
- Pre-commit hooks for linting and testing

Follow the git workflow section in CLAUDE.md
```

**EXPECTED RESULT:**
Git repository with proper branch structure and commit conventions

---

## Page 13: Step 1 - Write Specification

**PROMPT:**
```
I need to implement user authentication for my API.

Requirements:
- Users register with email/password
- JWT tokens for authentication
- Password hashing with bcrypt
- Token refresh endpoint
- Logout (token invalidation)

Database:
- users table: id, email, password_hash, created_at, updated_at

API Endpoints:
POST /api/auth/register - Register new user
POST /api/auth/login - Login and get JWT
POST /api/auth/refresh - Refresh JWT token
POST /api/auth/logout - Invalidate token

Please create the database migration first.
```

**EXPECTED RESULT:**
Claude asks clarifying questions and confirms the specification

---

## Page 15: Step 2 - Review Schema

**PROMPT:**
```
Review the migration file Claude created.

Check:
- Column types are appropriate
- Indexes are in place
- Constraints are correct

If approved, say: "Looks good, please proceed to repository layer"
If changes needed: "Change X to Y because..."

Run the migration:
psql -d mydb -f migrations/001_create_users.up.sql
```

**EXPECTED RESULT:**
Database table created successfully with proper indexes

---

## Page 17: Step 4 - Request API Implementation

**PROMPT:**
```
The repository layer looks good.

Now implement the API handlers:
1. POST /api/auth/register
   - Validate email format
   - Check password strength (min 8 chars)
   - Hash password with bcrypt
   - Return JWT token

2. POST /api/auth/login
   - Validate credentials
   - Compare password hash
   - Return JWT token

3. POST /api/auth/refresh
   - Validate existing token
   - Issue new token

Include error handling and proper HTTP status codes.
```

**EXPECTED RESULT:**
Claude creates handler files with validation and error handling

---

## Page 19: Step 5 - Request API Tests

**PROMPT:**
```
Create comprehensive E2E tests for the auth endpoints using Cypress.

Test cases:
1. Register - Happy path
2. Register - Duplicate email (409 error)
3. Register - Invalid email (400 error)
4. Register - Weak password (400 error)
5. Login - Valid credentials
6. Login - Invalid credentials (401 error)
7. Login - Non-existent user (401 error)
8. Refresh - Valid token
9. Refresh - Expired token (401 error)

Use Cypress API testing (cy.request)
```

**EXPECTED RESULT:**
Cypress test file created with all test cases

---

## Page 21: Run API Tests

**PROMPT:**
```
Run the API tests Claude created:

npx cypress run --spec "cypress/e2e/api/auth.cy.js"

Verify all tests pass.

If any fail, ask Claude:
"Test X is failing with error Y. Please investigate and fix.
```

**EXPECTED RESULT:**
All API tests pass (green checkmarks in terminal)

---

## Page 22: Step 6 - Request Frontend

**PROMPT:**
```
Now let's build the UI for authentication.

Create React components:
1. LoginForm component
   - Email and password inputs
   - Form validation
   - Submit calls /api/auth/login
   - Stores JWT in localStorage

2. RegisterForm component
   - Email, password, confirm password inputs
   - Client-side validation
   - Submit calls /api/auth/register
   - Auto-login after registration

Use React Hook Form for form handling and Zustand for auth state.
```

**EXPECTED RESULT:**
React components created with forms and state management

---

## Page 24: Step 7 - Request UI Tests

**PROMPT:**
```
Create UI E2E tests for the authentication flow.

Test scenarios:
1. User can register new account
2. User can login with valid credentials
3. User cannot login with invalid password
4. Form validation works (weak password, invalid email)
5. User stays logged in after page refresh
6. User can logout

Use data-test attributes for stable selectors.
```

**EXPECTED RESULT:**
Cypress UI test file created with user journey tests

---

## Page 28: Practice: Write E2E Test

**PROMPT:**
```
Write an E2E test for a password reset flow.

Feature requirements:
- User enters email on /forgot-password page
- System sends reset link to email
- User clicks link, enters new password
- User can login with new password

Create BOTH API and UI E2E tests for this flow.

Ask Claude to implement the feature + tests following the 10-step process.
```

**EXPECTED RESULT:**
Complete password reset feature with passing E2E tests

---

## Page 32: Practice: Proper Git Workflow

**PROMPT:**
```
You've implemented the auth feature. Now create a proper PR.

Steps:
1. Review your changes: git status, git diff
2. Run pre-commit checks (lint, tests, build)
3. Commit with conventional format
4. Push branch
5. Create PR with description

Ask Claude:
"Please help me commit the auth feature and create a PR.
Run all pre-commit checks first.
Use conventional commit format.
Include a detailed PR description.
```

**EXPECTED RESULT:**
PR created with passing CI checks and proper commit messages

---

## Page 34: Practice: Better Prompts

**PROMPT:**
```
Compare these two prompts:

❌ BAD:
"Add search to the users page"

✅ GOOD:
"Add search functionality to users page:
- Search input in page header
- Filter by email and name (case-insensitive)
- Debounce 300ms
- Update URL query params
- Clear button
- Show 'No results' when empty

Follow our existing search pattern from products page.
Include E2E test for search + clear + no results."

Practice: Write a detailed prompt for adding pagination.
```

**EXPECTED RESULT:**
You create a comprehensive, specific prompt with clear requirements

---

## Page 38: Final Exercise: Complete Feature

**PROMPT:**
```
Build a complete feature end-to-end:

Feature: User Profile Management
- View profile page showing user info
- Edit profile (name, email, avatar)
- Password change form
- Profile picture upload

Follow the full 10-step process:
1. Write specification (you)
2. Database schema (Claude → you review)
3. Repository layer (Claude → you review)
4. API endpoints (Claude → you review)
5. API E2E tests (Claude → you verify)
6. React components (Claude → you review)
7. UI E2E tests (Claude → you verify)
8. Documentation (Claude → you review)
9. Code review (you conduct)
10. Create PR (Claude → you merge)

Time limit: 30 minutes
```

**EXPECTED RESULT:**
Complete profile feature with passing tests and PR ready for review

---

## Page 44: EXERCISE: Multi-Phase Task Manager (Phase 0)

**PROMPT:**
```
Goal: Build a Task Management System across multiple phases

Phase 0: Foundation (We'll do this)
- User auth (Google OAuth + JWT)
- Organizations and teams
- Basic permissions

Phase 1: Projects (Demo only - out of scope)
- Project CRUD
- Project members
- Roles and permissions

Phase 2-3: Not implemented (Show planning only)

Step 1: Create Planning Structure
mkdir task-manager && cd task-manager
git init
mkdir -p project/{planning,specs,sessions,development}

Step 2: Ask Claude to create devplan.md
"Create project/planning/devplan.md for a Task Management System.

Break into 4 phases:
- Phase 0: Foundation (Auth, Users, Orgs)
- Phase 1: Projects (CRUD, Members)
- Phase 2: Tasks (CRUD, Comments, Attachments)
- Phase 3: Dashboard (Analytics)

For each phase list: DB tables, repos, API endpoints, UI pages, tests.
Use vertical slice workflow. Include checkboxes."

Expected: Complete devplan.md with ~80-100 tasks
```

**EXPECTED RESULT:**
devplan.md created with 4 phases and dependency mapping

---

## Page 45: EXERCISE: Create Progress Tracker

**PROMPT:**
```
Step 3: Create devprogress.md

"Create project/planning/devprogress.md based on devplan.md.

Add:
- Quick Stats table (4 phases with status indicators)
- Current Sprint section (Phase 0 - Foundation)
- Sprint Goals (5-7 goals for Phase 0)
- All Phase 0 tasks with checkboxes
- Set Phase 0 to '🟡 In Progress' with 0% initially
- Mark other phases as '🔴 Not Started'"

Expected: devprogress.md showing Phase 0 ready to start

Step 4: Create database.md

"Create project/planning/database.md with complete schema.

Tables: organizations, users, user_groups, permissions,
projects, project_members, tasks, comments, attachments

For each: columns, types, PKs, FKs, indexes, constraints"

Expected: Full database schema for all phases
```

**EXPECTED RESULT:**
devprogress.md and database.md created

---

## Page 46: EXERCISE: Implement Phase 0 Database

**PROMPT:**
```
Step 5: Database Migrations

"I'm in api/ directory. Initialize Go project and create migrations.

- Create go.mod for 'task-manager-api'
- Create: cmd/api, internal/{handlers,middleware,models,repository}, migrations/
- Create migrations for Phase 0 tables:
  001_create_organizations.up.sql
  002_create_users.up.sql
  003_create_user_groups.up.sql
  004_create_permissions.up.sql

Include seed data:
- Default organization
- Admin user group
- Permissions: users:*, projects:*, tasks:*"

Expected: Go project initialized, 4 migrations created

Step 6: Update Progress

"Update project/planning/devprogress.md:
- Mark database setup tasks as [x]
- Update Phase 0 percentage
- Update 'Completed This Session'"

Expected: Progress tracker shows ~20-30% Phase 0 complete
```

**EXPECTED RESULT:**
Migrations created and progress updated

---

## Page 47: EXERCISE: Implement Auth System

**PROMPT:**
```
Step 7: Google OAuth + JWT

"Implement Google OAuth + JWT authentication:

1. models/user.go - User struct
2. repository/user_repository.go - GetByID, GetByEmail, Create, Update
3. handlers/auth_handler.go - GoogleLogin, GoogleCallback, GetMe
4. middleware/auth.go - JWT validation
5. cmd/api/main.go - Routes

Dependencies: gorilla/mux, golang-jwt/jwt/v5, lib/pq, oauth2/google
Use repository pattern - handlers never touch DB directly."

Expected: Auth system with OAuth and JWT

Step 8: Update Progress Again

"Update devprogress.md:
- Mark auth, repository, API tasks as [x]
- Update Phase 0 percentage
- Add to 'Completed This Session'"

Expected: Progress shows ~60-70% Phase 0 complete
```

**EXPECTED RESULT:**
Auth implemented and progress updated

---


# AI-First Workshop Prompts

Copy and paste these prompts during the workshop exercises.

---

## Page 9: Exercise 1: Create Your Repository

**PROMPT:**
```
Create a new GitHub repository for your project:

1. Go to github.com and create a new PRIVATE repository
   Name: my-ai-project (or your preferred name)

2. Clone it locally:
   git clone https://github.com/[YOUR-USERNAME]/my-ai-project.git
   cd my-ai-project

3. Verify:
   git status
   Should show: "On branch main, nothing to commit"

Reference: Check unveiling-claude repo structure for ideas
```

**EXPECTED RESULT:**
Local repository initialized and connected to GitHub

---

## Page 10: Exercise 2: Create Project Rules File

**PROMPT:**
```
Ask your AI assistant:

Help me create a project rules file for my project.

Project details:
- Language: [Go/Node/Python]
- Type: REST API with database
- Database: PostgreSQL (or SQLite for simplicity)
- Testing: E2E with [Cypress/Go test/pytest]

Include these sections:
1. Project Overview (what this project does)
2. Tech Stack (language, framework, database)
3. Project Structure (recommended directories)
4. Commands (build, test, run)
5. Git Workflow (branch naming, commit format)
6. Testing Requirements (E2E mandatory)

Save as CLAUDE.md (or .windsurfrules for Windsurf)
```

**EXPECTED RESULT:**
Project rules file created with all sections

---

## Page 12: Exercise 3: Initialize Git Workflow

**PROMPT:**
```
Ask your AI assistant:

Set up the git workflow for my project:

1. Create .gitignore for [Go/Node/Python] project
   Include: build outputs, dependencies, IDE files, .env

2. Create initial directory structure:
   - cmd/ or src/ for source code
   - tests/ or test/ for tests
   - migrations/ for database migrations
   - docs/ for documentation

3. Create initial commit:
   git add .
   git commit -m "chore: initial project setup"

4. Create feature branch for our first feature:
   git checkout -b feature/user-auth
```

**EXPECTED RESULT:**
Git initialized with proper structure and on feature branch

---

## Page 16: Step 1: Write Feature Specification

**PROMPT:**
```
Ask your AI assistant:

I need to implement user authentication for my API.

Requirements:
- Users register with email and password
- Users login with email and password
- JWT tokens for authentication
- Password hashing (never store plain text)

Database Schema Needed:
- users table: id, email, password_hash, created_at, updated_at

API Endpoints:
POST /api/auth/register - Register new user
  Request: { email, password }
  Response: { user_id, email, token }

POST /api/auth/login - Login existing user
  Request: { email, password }
  Response: { user_id, email, token }

Success Criteria:
- Passwords hashed with bcrypt
- JWT expires after 1 hour
- Proper HTTP status codes (201, 200, 400, 401)
- E2E tests cover happy path and errors

Please confirm you understand before we proceed.
```

**EXPECTED RESULT:**
AI confirms understanding, may ask clarifying questions

---

## Page 18: Step 2: Create Database Schema

**PROMPT:**
```
Ask your AI assistant:

Create the database migration for the users table.

Requirements:
- Table name: users
- Columns: id (primary key), email (unique), password_hash, created_at, updated_at
- Add index on email column for fast lookups

For Go: Create migrations/001_create_users.up.sql and .down.sql
For Node: Create migrations/001_create_users.js
For Python: Create migrations/001_create_users.py

Use appropriate types for your database:
- PostgreSQL: SERIAL, VARCHAR, TIMESTAMP
- SQLite: INTEGER PRIMARY KEY, TEXT

Include both up (create) and down (drop) migrations.
```

**EXPECTED RESULT:**
Migration file(s) created with proper schema

---

## Page 21: Step 3: Implement Repository Layer

**PROMPT:**
```
Ask your AI assistant:

Implement the repository layer for user operations.

Create a UserRepository with these methods:
- Create(email, passwordHash) -> User
- FindByEmail(email) -> User or null
- FindByID(id) -> User or null

Requirements:
- Use prepared statements (prevent SQL injection)
- Handle database errors gracefully
- Return appropriate errors (not found, duplicate, etc.)

Place in:
- Go: internal/repository/user_repository.go
- Node: src/repositories/userRepository.js
- Python: app/repositories/user_repository.py

Follow patterns from the project rules file.
```

**EXPECTED RESULT:**
Repository file created with all methods

---

## Page 22: Step 4: Implement API Handlers

**PROMPT:**
```
Ask your AI assistant:

Implement the API handlers for authentication.

Create handlers for:
1. POST /api/auth/register
   - Validate email format
   - Validate password (minimum 8 characters)
   - Hash password with bcrypt
   - Create user in database
   - Generate and return JWT token
   - Return 400 for validation errors
   - Return 409 for duplicate email

2. POST /api/auth/login
   - Find user by email
   - Verify password against hash
   - Generate and return JWT token
   - Return 401 for invalid credentials

Include:
- Input validation
- Proper HTTP status codes
- JSON response format: { success: true/false, data/error }
- Wire up routes to main application
```

**EXPECTED RESULT:**
Handler files created and routes configured

---

## Page 25: Step 5: Write E2E API Tests

**PROMPT:**
```
Ask your AI assistant:

Create E2E tests for the authentication endpoints.

Test cases needed:
1. Register - Happy path (201)
   - New user can register
   - Response includes token

2. Register - Duplicate email (409)
   - Cannot register same email twice

3. Register - Invalid email (400)
   - Rejects malformed email

4. Register - Weak password (400)
   - Rejects password < 8 chars

5. Login - Valid credentials (200)
   - Returns token

6. Login - Invalid password (401)
   - Wrong password rejected

7. Login - Non-existent user (401)
   - Unknown email rejected

Use your testing framework:
- Go: internal/handlers/auth_test.go
- Node: tests/api/auth.test.js (Jest/Vitest)
- Python: tests/test_auth.py (pytest)

Include setup and teardown for test database.
```

**EXPECTED RESULT:**
Test file created with all test cases

---

## Page 27: Run and Verify Tests

**PROMPT:**
```
Run your E2E tests:

For Go:
  go test -v ./internal/handlers/...

For Node:
  npm test -- --grep "Auth API"

For Python:
  pytest tests/test_auth.py -v

Expected: All 7 test cases pass (green)

If tests fail, share the error with your AI assistant:
"Test [name] is failing with this error:
[paste error output]

Please analyze the failure and suggest a fix."

Continue until ALL tests pass!
```

**EXPECTED RESULT:**
All E2E tests passing (7/7 green)

---

## Page 31: Exercise: Add Unit Tests

**PROMPT:**
```
Ask your AI assistant:

Add unit tests for the authentication logic.

Create unit tests for:
1. Password validation function
   - Test: 8+ chars passes
   - Test: < 8 chars fails
   - Test: Empty string fails

2. Email validation function
   - Test: valid@email.com passes
   - Test: invalid-email fails
   - Test: Empty string fails

3. JWT token generation
   - Test: Token contains user ID
   - Test: Token has correct expiration

4. Password hashing
   - Test: Same password produces different hashes (salt)
   - Test: Verify function works

Place in appropriate test file:
- Go: internal/auth/auth_test.go
- Node: tests/unit/auth.test.js
- Python: tests/unit/test_auth.py
```

**EXPECTED RESULT:**
Unit tests created and passing

---

## Page 35: Exercise: Create Proper Commits

**PROMPT:**
```
Ask your AI assistant:

Help me commit my authentication feature properly.

My changes include:
- Database migration for users table
- Repository layer
- API handlers
- E2E tests
- Unit tests

Steps:
1. Review what's changed: git status
2. Stage all changes: git add .
3. Create commit with conventional format

Suggested commit message:
feat(auth): add user registration and login

- Add users table migration
- Implement user repository with CRUD
- Create register and login endpoints
- Add E2E tests for all auth endpoints
- Add unit tests for validation logic

After committing, verify with: git log --oneline -1
```

**EXPECTED RESULT:**
Commit created with proper conventional commit message

---

## Page 36: Exercise: Create Pull Request

**PROMPT:**
```
Ask your AI assistant:

Help me push my branch and create a pull request.

Steps:
1. Push branch to remote:
   git push -u origin feature/user-auth

2. Create PR (with GitHub CLI):
   gh pr create --title "feat: Add user authentication" \
     --body "## Summary
   - User registration endpoint
   - User login endpoint
   - JWT token authentication
   - E2E tests (7 passing)
   - Unit tests for validation

   ## Testing
   - All E2E tests pass
   - All unit tests pass
   - Manual testing completed

   ## Checklist
   - [x] Code follows project conventions
   - [x] Tests added
   - [x] Documentation updated"

Or create PR through GitHub web interface.
```

**EXPECTED RESULT:**
PR created on GitHub with description

---

## Page 41: Final Challenge: Your Feature

**PROMPT:**
```
Choose ONE feature and implement it fully:

OPTION A: GET /api/auth/me
- Returns current user info from JWT token
- Response: { id, email, created_at }
- Tests: valid token returns user, invalid token returns 401

OPTION B: PUT /api/auth/password
- Request: { current_password, new_password }
- Verify current password, update to new
- Tests: success, wrong current password, weak new password

OPTION C: POST /api/auth/logout
- Invalidate current token (add to blacklist)
- Tests: logout succeeds, token no longer works

Steps:
1. Tell AI which feature you chose
2. Have AI implement it
3. Review the code
4. Run tests
5. Commit with conventional format

Time limit: 25 minutes
```

**EXPECTED RESULT:**
New feature implemented with passing tests and committed

---


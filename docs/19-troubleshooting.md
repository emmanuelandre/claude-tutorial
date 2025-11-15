# Troubleshooting Guide

Common issues and solutions when working with Claude Code.

## General Issues

### Claude Doesn't Understand Context

**Problem:**
Claude seems to ignore project conventions or makes incorrect assumptions.

**Solution:**
1. Check CLAUDE.md exists and is up to date
2. Explicitly reference CLAUDE.md in your prompt:
   ```
   "Following our CLAUDE.md conventions, implement..."
   ```
3. Provide specific file paths and examples
4. Start sessions with context:
   ```
   "Working on the authentication feature. We use JWT tokens
    and follow the patterns in src/auth/. I need to..."
   ```

### AI Generates Code That Doesn't Match Project Style

**Problem:**
Code uses different conventions than your project.

**Solution:**
1. Update CLAUDE.md with specific conventions:
   ```markdown
   ## Code Style
   - Use single quotes for strings
   - 2-space indentation
   - Semicolons required
   - Trailing commas in arrays/objects
   ```
2. Reference existing code:
   ```
   "Follow the same pattern as in src/services/UserService.js"
   ```
3. Provide code examples in CLAUDE.md

### Claude Creates Too Many Unit Tests

**Problem:**
AI generates extensive unit tests when E2E tests would be better.

**Solution:**
1. Update CLAUDE.md with testing strategy:
   ```markdown
   ## Testing Strategy
   - Prioritize E2E tests over unit tests
   - Unit tests only for complex algorithms
   - All features must have E2E tests
   ```
2. Be explicit in requests:
   ```
   "Implement this feature with comprehensive E2E tests.
    Skip unit tests unless there's a clear reason."
   ```

## Git and Version Control

### Cannot Push to Main Branch

**Problem:**
```
remote: error: GH013: Repository rule violations found for refs/heads/main
```

**Solution:**
This is correct! Never push directly to main.

```bash
# Create feature branch
git checkout -b feature/my-feature

# Push to feature branch
git push -u origin feature/my-feature

# Create PR
gh pr create
```

### Merge Conflicts

**Problem:**
Git shows merge conflicts when pulling or merging.

**Solution:**
```bash
# Update your branch from main
git checkout feature/my-feature
git fetch origin
git rebase origin/main

# If conflicts occur
# 1. Edit conflicted files (look for <<<<<<< markers)
# 2. Resolve conflicts
git add .
git rebase --continue

# Force push (since history changed)
git push --force-with-lease
```

### Accidentally Committed to Wrong Branch

**Problem:**
Committed to main instead of feature branch.

**Solution:**
```bash
# Don't push!
# Create feature branch from current state
git checkout -b feature/my-feature

# Reset main to remote state
git checkout main
git reset --hard origin/main

# Your changes are now on feature branch
git checkout feature/my-feature
```

## Testing Issues

### E2E Tests Failing Intermittently

**Problem:**
Tests pass sometimes, fail other times.

**Solution:**

**1. Add proper waits:**
```javascript
❌ // Don't do this
cy.get('[data-test="submit"]').click()
cy.get('[data-test="success"]').should('be.visible')

✅ // Do this
cy.get('[data-test="submit"]').click()
cy.get('[data-test="success"]', { timeout: 10000 })
  .should('be.visible')
```

**2. Wait for API calls:**
```javascript
cy.intercept('POST', '/api/v1/users').as('createUser')
cy.get('[data-test="submit"]').click()
cy.wait('@createUser')
cy.get('[data-test="success"]').should('be.visible')
```

**3. Ensure clean state:**
```javascript
beforeEach(() => {
  cy.task('db:reset')  // Reset database
  cy.clearCookies()
  cy.clearLocalStorage()
})
```

### Tests Pass Locally But Fail in CI

**Problem:**
All tests pass on your machine but fail in GitHub Actions/CI.

**Solution:**

**1. Check environment variables:**
```yaml
# .github/workflows/test.yml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_URL: http://localhost:8080
```

**2. Verify database setup:**
```yaml
jobs:
  test:
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
```

**3. Add debugging:**
```javascript
cy.on('fail', (error) => {
  console.log('Test failed:', error.message)
  cy.screenshot('failure')
})
```

### Test Data Leaking Between Tests

**Problem:**
Tests fail because of data from previous tests.

**Solution:**
```javascript
// Option 1: Reset database before each test
beforeEach(() => {
  cy.task('db:reset')
})

// Option 2: Use unique data
const createUniqueUser = () => ({
  email: `user-${Date.now()}@example.com`,
  name: `User ${Date.now()}`
})

// Option 3: Clean up after each test
afterEach(() => {
  cy.task('db:cleanup', { table: 'users' })
})
```

## Development Workflow Issues

### Pre-commit Hooks Failing

**Problem:**
```
✖ npm run lint
  Error: ESLint errors found
```

**Solution:**

**1. Auto-fix linting:**
```bash
npm run lint --fix
```

**2. Check formatting:**
```bash
npm run format
```

**3. Verify build:**
```bash
npm run build
```

**4. Only commit when all checks pass:**
```bash
# Run all checks
npm run lint && npm test && npm run build

# If all pass, commit
git commit -m "feat: add feature"
```

### Build Fails After Pulling Latest Changes

**Problem:**
```
Error: Cannot find module 'some-package'
```

**Solution:**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# For Go
go mod download
go mod tidy

# For Python
pip install -r requirements.txt
```

### Environment Variables Not Loading

**Problem:**
Application can't find environment variables.

**Solution:**

**1. Check .env file exists:**
```bash
ls -la .env
```

**2. Verify .env format:**
```bash
# Correct
DATABASE_URL=postgresql://localhost/mydb
API_KEY=abc123

# Wrong (no spaces around =)
DATABASE_URL = postgresql://localhost/mydb
```

**3. Load in development:**
```javascript
// Node.js
require('dotenv').config()

// Or in package.json
"dev": "node -r dotenv/config src/index.js"
```

## API and Backend Issues

### CORS Errors

**Problem:**
```
Access to fetch at 'http://localhost:8080/api/users' from origin
'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**

**Backend (Go):**
```go
import "github.com/rs/cors"

handler := cors.New(cors.Options{
    AllowedOrigins:   []string{"http://localhost:3000"},
    AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE"},
    AllowedHeaders:   []string{"Content-Type", "Authorization"},
    AllowCredentials: true,
}).Handler(router)
```

**Backend (Node.js/Express):**
```javascript
const cors = require('cors')

app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}))
```

### Database Connection Errors

**Problem:**
```
Error: connect ECONNREFUSED 127.0.0.1:5432
```

**Solution:**

**1. Check database is running:**
```bash
# Docker
docker ps | grep postgres

# Or start it
docker-compose up -d postgres
```

**2. Verify connection string:**
```bash
# Check .env
cat .env | grep DATABASE_URL

# Test connection
psql "postgresql://user:pass@localhost:5432/dbname"
```

**3. Check credentials:**
```sql
-- Connect as postgres user
psql -U postgres

-- List databases
\l

-- Check user permissions
\du
```

### JWT Token Expired

**Problem:**
```
401 Unauthorized: Token expired
```

**Solution:**

**1. Implement token refresh:**
```javascript
// API client
async function refreshToken() {
  const response = await fetch('/api/v1/auth/refresh', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('refreshToken')}`
    }
  })
  const { token } = await response.json()
  localStorage.setItem('token', token)
  return token
}

// Retry failed requests with new token
async function fetchWithRetry(url, options) {
  let response = await fetch(url, options)

  if (response.status === 401) {
    // Refresh token and retry
    const newToken = await refreshToken()
    options.headers.Authorization = `Bearer ${newToken}`
    response = await fetch(url, options)
  }

  return response
}
```

## Frontend Issues

### React Component Not Re-rendering

**Problem:**
State updates but UI doesn't change.

**Solution:**

**1. Check state mutation:**
```javascript
❌ // Mutating state directly
const addItem = (item) => {
  items.push(item)
  setItems(items)  // Won't trigger re-render
}

✅ // Create new array
const addItem = (item) => {
  setItems([...items, item])  // Triggers re-render
}
```

**2. Use functional updates:**
```javascript
❌ // May use stale state
const increment = () => {
  setCount(count + 1)
}

✅ // Always uses current state
const increment = () => {
  setCount(prev => prev + 1)
}
```

### Infinite Loop in useEffect

**Problem:**
Component re-renders infinitely.

**Solution:**
```javascript
❌ // Missing dependency or wrong dependency
useEffect(() => {
  fetchData()
}, [])  // fetchData changes on every render

✅ // Correct dependencies
useEffect(() => {
  fetchData()
}, [userId])  // Only when userId changes

// Or use useCallback
const fetchData = useCallback(() => {
  // fetch logic
}, [userId])

useEffect(() => {
  fetchData()
}, [fetchData])
```

### Bundle Size Too Large

**Problem:**
Production build is multiple megabytes.

**Solution:**

**1. Code splitting:**
```javascript
// Use dynamic imports
const Dashboard = lazy(() => import('./pages/Dashboard'))

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

**2. Analyze bundle:**
```bash
npm install --save-dev webpack-bundle-analyzer

# Add to webpack config
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

plugins: [
  new BundleAnalyzerPlugin()
]

npm run build
```

**3. Remove unused dependencies:**
```bash
npm prune
```

## Docker and Deployment Issues

### Docker Build Fails

**Problem:**
```
ERROR [stage-1 5/5] RUN npm run build
```

**Solution:**

**1. Check .dockerignore:**
```
node_modules
npm-debug.log
.env
.git
```

**2. Verify Dockerfile:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm ci --production

# Then copy source
COPY . .

RUN npm run build

CMD ["npm", "start"]
```

### Container Can't Connect to Database

**Problem:**
```
Error: connect ECONNREFUSED 127.0.0.1:5432
```

**Solution:**

Use service name from docker-compose:
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15

  api:
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/dbname
      # Use 'postgres' not 'localhost'
```

### Port Already in Use

**Problem:**
```
Error: listen EADDRINUSE: address already in use :::8080
```

**Solution:**
```bash
# Find process using port
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port
docker-compose up -d --build
```

## Claude Code Specific Issues

### Claude Refuses to Make Changes

**Problem:**
Claude says it can't make the change.

**Solution:**

**1. Be more specific:**
```
❌ "Fix the bug"
✅ "In src/auth.js line 45, change the token expiry from
   1 hour to 24 hours"
```

**2. Break down the request:**
```
"Let's fix this in steps:
1. First, show me the current code
2. Identify the bug
3. Propose a fix
4. Implement the fix"
```

### Claude Suggests Wrong Technology

**Problem:**
Claude suggests using library X but you use library Y.

**Solution:**
Update CLAUDE.md:
```markdown
## Tech Stack
- Frontend: React 18 with React Router v6
- State Management: Zustand (NOT Redux)
- Forms: React Hook Form (NOT Formik)
- HTTP: Axios (NOT fetch)
```

## Getting More Help

### Documentation
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [GitHub Issues](https://github.com/anthropics/claude-code/issues)

### Community
- [Discord Community](#)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/claude-code)

### Debugging Tips

**1. Be systematic:**
- Identify exact error message
- Find where error occurs
- Check recent changes
- Test in isolation

**2. Use debugging tools:**
- Browser DevTools
- VSCode debugger
- `console.log` strategically
- Cypress test runner

**3. Ask for help effectively:**
```
"I'm seeing this error:
[paste exact error]

When I:
[steps to reproduce]

I expected:
[expected behavior]

But got:
[actual behavior]

I've tried:
[what you've attempted]

Relevant code:
[paste code snippet]"
```

---

**Prev:** [Advanced Topics](./18-advanced-topics.md) | **Next:** [Tips & Tricks](./20-tips-tricks.md)

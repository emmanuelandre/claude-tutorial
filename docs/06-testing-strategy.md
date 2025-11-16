# Testing Strategy

Modern testing philosophy for AI-first development.

## Core Philosophy

**Comprehensive Testing: E2E + Unit Tests (Both Mandatory) + Component Tests (Good to Have)**

### Modern Testing Approach

Traditional testing pyramid (bottom-heavy):
```
      /\
     /  \ ← E2E (few)
    /────\
   /      \ ← Integration (some)
  /────────\
 /          \ ← Unit (many)
/__Unit Tests__\
```

Modern comprehensive testing (balanced with emphasis on E2E):
```
  ____________
 /            \ ← E2E (comprehensive & mandatory)
/__E2E Tests__\
  ____________
 /            \ ← Unit Tests (mandatory)
/__Unit Tests_\
  /          \ ← Component (good to have)
 /────────────\
  /  Test   \ ← Test Containers for microservices
 /_Containers_\
```

### Why This Works

**E2E Tests:**
- ✅ Test actual user flows
- ✅ Catch integration issues
- ✅ Verify the whole system
- ✅ Document expected behavior
- ✅ Enable confident refactoring

**Unit Tests:**
- ✅ Test business logic in isolation
- ✅ Fast feedback during development
- ✅ Catch edge cases and boundary conditions
- ✅ Enable confident refactoring of internal logic
- ✅ Mandatory for quality assurance

**Component Tests:**
- ✅ Test integration between components
- ✅ Use test containers (Testcontainers) for microservices
- ✅ Verify database, message queues, external services
- ✅ Good to have where applicable (not all code is microservices)
- ⚠️ Not always necessary for simple applications

## Test-First Approach with Coverage Measurement

**Both E2E and Unit Tests Are Mandatory**

The modern approach combines the strengths of both testing strategies:

### Coverage-Driven Development

1. **Define coverage targets before implementation**
   - Set minimum coverage thresholds (typically 70-90%)
   - Higher coverage = higher confidence
   - Thresholds vary by project criticality

2. **Build testing infrastructure first**
   - Set up E2E testing framework (Cypress, Playwright)
   - Configure unit test runners (Jest, Vitest, Go testing)
   - Set up component testing with test containers (if applicable)
   - Configure coverage reporting tools for all test types

3. **Track coverage from all test types**
   - Unit test coverage (line, branch, function coverage)
     - JavaScript/TypeScript: `jest --coverage` or `vitest --coverage`
     - Go: `go test -coverprofile=coverage.out ./...`
   - E2E test coverage (code coverage from E2E tests)
     - Cypress: `@cypress/code-coverage` plugin
     - Playwright: `@playwright/test` with coverage instrumentation
   - Component test coverage (integration points)
   - Combined coverage report (merge unit + E2E + component coverage)

### What to Test Where

**Unit Tests (Mandatory):**
- Business logic and algorithms
- Utility functions and helpers
- Edge cases and boundary conditions
- Data transformations and validators
- Error handling paths
- Pure functions and calculations

**E2E Tests (Mandatory):**
- Complete user journeys
- API endpoints (request → response)
- UI workflows (login → action → result)
- Authentication and authorization flows
- Data persistence verification
- Integration between all system components

**Component Tests (Good to Have):**
- Microservices integration (use Testcontainers)
- Database operations (with test DB containers)
- Message queue interactions
- External service mocks
- Note: Not applicable for all projects (e.g., simple monoliths)

## E2E Testing Best Practices

### 1. Test User Journeys, Not Functions

❌ **Wrong:**
```javascript
// Testing implementation details
test('formatDate function formats correctly', () => {
  expect(formatDate('2024-01-15')).toBe('Jan 15, 2024')
})
```

✅ **Right:**
```javascript
// Testing user behavior
test('user can view formatted dates on dashboard', () => {
  cy.visit('/dashboard')
  cy.get('[data-test="created-date"]')
    .should('contain', 'Jan 15, 2024')
})
```

### 2. Cover Happy Path and Critical Failures

**Minimum E2E Coverage:**

```javascript
// Feature: User Registration

// Happy path
test('user can register successfully', () => {
  cy.visit('/register')
  cy.get('[data-test="email"]').type('user@example.com')
  cy.get('[data-test="password"]').type('SecurePass123!')
  cy.get('[data-test="submit"]').click()

  cy.url().should('include', '/dashboard')
  cy.contains('Welcome').should('be.visible')
})

// Critical failures
test('shows error for duplicate email', () => {
  // ... register first user
  // ... try registering with same email
  cy.contains('Email already registered').should('be.visible')
})

test('shows error for weak password', () => {
  cy.visit('/register')
  cy.get('[data-test="password"]').type('weak')
  cy.get('[data-test="submit"]').click()

  cy.contains('Password must be at least 8 characters')
    .should('be.visible')
})

test('shows error when server is down', () => {
  cy.intercept('POST', '/api/register', {
    statusCode: 500,
    body: { error: 'Server error' }
  })

  // ... attempt registration
  cy.contains('Registration failed').should('be.visible')
})
```

### 3. Use Data Attributes for Selectors

❌ **Fragile:**
```javascript
cy.get('.btn-primary').click()
cy.get('div > form > input:nth-child(2)').type('test')
```

✅ **Stable:**
```javascript
cy.get('[data-test="submit-button"]').click()
cy.get('[data-test="email-input"]').type('test')
```

**In your HTML:**
```html
<button data-test="submit-button" class="btn-primary">
  Submit
</button>

<input data-test="email-input" type="email" />
```

### 4. Create Reusable Commands

```javascript
// cypress/support/commands.js

Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login')
  cy.get('[data-test="email"]').type(email)
  cy.get('[data-test="password"]').type(password)
  cy.get('[data-test="submit"]').click()
  cy.url().should('include', '/dashboard')
})

Cypress.Commands.add('createStrategy', (name, config) => {
  cy.request({
    method: 'POST',
    url: '/api/v1/strategies',
    body: { name, config },
    headers: {
      'Authorization': `Bearer ${Cypress.env('authToken')}`
    }
  })
})

// Usage in tests
cy.login('user@example.com', 'password')
cy.createStrategy('My Strategy', { type: 'momentum' })
```

### 5. Test API and UI Separately

**API E2E Tests:**
```javascript
describe('API: Strategy Management', () => {
  test('POST /api/v1/strategies creates strategy', () => {
    cy.request({
      method: 'POST',
      url: '/api/v1/strategies',
      body: {
        name: 'Test Strategy',
        description: 'Test',
        config: { type: 'momentum' }
      }
    }).then((response) => {
      expect(response.status).to.eq(201)
      expect(response.body).to.have.property('id')
      expect(response.body.name).to.eq('Test Strategy')
    })
  })

  test('GET /api/v1/strategies returns strategies', () => {
    cy.request('/api/v1/strategies')
      .its('body')
      .should('be.an', 'array')
  })
})
```

**UI E2E Tests:**
```javascript
describe('UI: Strategy Management', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password')
  })

  test('user can create strategy via UI', () => {
    cy.visit('/strategies')
    cy.get('[data-test="new-strategy"]').click()
    cy.get('[data-test="name"]').type('Test Strategy')
    cy.get('[data-test="submit"]').click()

    cy.contains('Strategy created').should('be.visible')
    cy.contains('Test Strategy').should('be.visible')
  })
})
```

### 6. Measure E2E Test Coverage

E2E tests should also contribute to code coverage metrics.

**Setup Cypress Code Coverage:**

```bash
# Install dependencies
npm install --save-dev @cypress/code-coverage nyc istanbul-lib-coverage

# Install babel plugin for instrumentation
npm install --save-dev babel-plugin-istanbul
```

**Configure babel.config.js:**

```javascript
module.exports = {
  presets: ['@babel/preset-env', '@babel/preset-react'],
  plugins: [
    process.env.NODE_ENV === 'test' && 'istanbul'
  ].filter(Boolean)
}
```

**Configure cypress.config.js:**

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

**Run E2E tests with coverage:**

```bash
# Run tests (coverage collected automatically)
npm run test:e2e

# View coverage report
npx nyc report --reporter=html
open coverage/index.html
```

**Merge Unit + E2E Coverage:**

```bash
# Merge coverage reports
npx nyc merge .nyc_output coverage/merged-coverage.json
npx nyc report --reporter=html --reporter=text --temp-dir=coverage

# View combined coverage
open coverage/index.html
```

## Component Testing (When Needed)

Use component tests for complex UI logic that's hard to test E2E.

### Example: Complex Form Validation

```javascript
// Component test for date range validator
test('date range validates correctly', () => {
  const { getByLabelText, getByText } = render(<DateRangePicker />)

  const startDate = getByLabelText('Start Date')
  const endDate = getByLabelText('End Date')

  // End date before start date
  fireEvent.change(startDate, { target: { value: '2024-01-15' } })
  fireEvent.change(endDate, { target: { value: '2024-01-10' } })

  expect(getByText('End date must be after start date'))
    .toBeInTheDocument()
})
```

### Example: Complex State Machine

```javascript
// Component test for multi-step wizard
test('wizard progresses through steps correctly', () => {
  const { getByText, queryByText } = render(<Wizard />)

  // Step 1 visible
  expect(getByText('Step 1: Basic Info')).toBeInTheDocument()
  expect(queryByText('Step 2: Configuration')).not.toBeInTheDocument()

  // Proceed to step 2
  fireEvent.click(getByText('Next'))
  expect(queryByText('Step 1: Basic Info')).not.toBeInTheDocument()
  expect(getByText('Step 2: Configuration')).toBeInTheDocument()
})
```

## Unit Testing Best Practices

Unit tests are mandatory and provide fast feedback during development.

### Example: Testing Business Logic

```javascript
// Utility function with complex logic
function calculatePortfolioMetrics(trades, prices) {
  // Complex calculation with edge cases
  // ...
}

// Unit test is valuable here
test('calculates Sharpe ratio correctly', () => {
  const trades = [/* mock data */]
  const prices = [/* mock data */]

  const result = calculatePortfolioMetrics(trades, prices)

  expect(result.sharpeRatio).toBeCloseTo(1.42, 2)
})

test('handles empty trades array', () => {
  const result = calculatePortfolioMetrics([], [])
  expect(result).toEqual({ sharpeRatio: 0, returns: 0 })
})
```

### Example: Testing Validation Logic

```javascript
// Validator function
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

function validatePassword(password) {
  return password.length >= 8 &&
         /[A-Z]/.test(password) &&
         /[0-9]/.test(password)
}

// Unit tests for validators
test('validates correct email format', () => {
  expect(validateEmail('user@example.com')).toBe(true)
  expect(validateEmail('invalid.email')).toBe(false)
  expect(validateEmail('missing@domain')).toBe(false)
})

test('validates password requirements', () => {
  expect(validatePassword('Short1')).toBe(false)        // Too short
  expect(validatePassword('NoNumbers')).toBe(false)     // No numbers
  expect(validatePassword('nonumber1')).toBe(false)     // No uppercase
  expect(validatePassword('ValidPass1')).toBe(true)     // Valid
})
```

### What About Database Operations?

For database operations, use **component tests with test containers** instead of mocking:

```javascript
✅ // Component test with Testcontainer
test('UserRepository.findById returns user', async () => {
  // Testcontainer spins up real PostgreSQL
  const container = await new PostgreSqlContainer().start()
  const repo = new UserRepository(container.getConnectionString())

  await repo.create({ email: 'test@example.com', name: 'Test User' })
  const user = await repo.findById(1)

  expect(user.email).toBe('test@example.com')

  await container.stop()
})
```

For simple CRUD without complex logic, E2E tests may be sufficient.

## Test Organization

### Directory Structure

```
project/
├── tests/
│   ├── e2e/
│   │   ├── api/           # API E2E tests
│   │   │   ├── auth.cy.js
│   │   │   ├── strategies.cy.js
│   │   │   └── backtests.cy.js
│   │   ├── ui/            # UI E2E tests
│   │   │   ├── login.cy.js
│   │   │   ├── dashboard.cy.js
│   │   │   └── strategies.cy.js
│   │   └── fixtures/      # Test data
│   │       ├── users.json
│   │       └── strategies.json
│   ├── component/         # Component tests (optional)
│   │   └── DatePicker.test.js
│   └── unit/              # Unit tests (rare)
│       └── calculations.test.js
└── cypress.config.js
```

### Naming Conventions

**E2E Tests:**
```
[feature].[domain].cy.js

Examples:
auth.api.cy.js
strategies.api.cy.js
dashboard.ui.cy.js
```

**Component Tests:**
```
[Component].test.js

Examples:
DatePicker.test.js
Wizard.test.js
```

**Unit Tests:**
```
[module].test.js

Examples:
calculations.test.js
validators.test.js
```

## Test Data Management

### Fixtures for Consistent Data

```javascript
// cypress/fixtures/users.json
{
  "admin": {
    "email": "admin@example.com",
    "password": "AdminPass123!",
    "role": "admin"
  },
  "user": {
    "email": "user@example.com",
    "password": "UserPass123!",
    "role": "user"
  }
}

// In tests
cy.fixture('users').then((users) => {
  cy.login(users.admin.email, users.admin.password)
})
```

### Factories for Dynamic Data

```javascript
// cypress/support/factories.js
export const createUser = (overrides = {}) => ({
  email: `user-${Date.now()}@example.com`,
  password: 'TestPass123!',
  name: 'Test User',
  ...overrides
})

export const createStrategy = (overrides = {}) => ({
  name: `Strategy ${Date.now()}`,
  description: 'Test strategy',
  config: { type: 'momentum' },
  ...overrides
})

// In tests
const user = createUser({ email: 'specific@example.com' })
const strategy = createStrategy({ name: 'My Strategy' })
```

## CI/CD Integration

### Run Tests in Pipeline

```yaml
# .github/workflows/test.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup
        run: |
          npm install
          npm run build

      - name: Run API E2E Tests
        run: npm run test:e2e:api

      - name: Run UI E2E Tests
        run: npm run test:e2e:ui

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: cypress/results
```

### Test Gates

**Merge Requirements:**
- ✅ All E2E tests pass
- ✅ All unit tests pass
- ✅ Coverage thresholds met (typically 70-90%)
- ✅ No console errors
- ✅ Build succeeds
- ✅ Lint checks pass

## Debugging Failed Tests

### 1. Screenshots and Videos

Cypress automatically captures these on failure:
```
cypress/
├── screenshots/
│   └── failed-test.png
└── videos/
    └── test-run.mp4
```

### 2. Debug Mode

```javascript
// Add .debug() to pause execution
cy.get('[data-test="submit"]').debug().click()

// Or use debugger
cy.get('[data-test="submit"]').then(() => {
  debugger  // Opens browser DevTools
})
```

### 3. Verbose Logging

```javascript
// Log intermediate values
cy.get('[data-test="total"]').then(($el) => {
  cy.log('Total value:', $el.text())
})
```

## Best Practices Summary

✅ **DO:**
- Write comprehensive E2E tests for all user journeys
- Write unit tests for business logic, utilities, and edge cases
- Use component tests with test containers for microservices
- Measure and track coverage from all test types
- Define coverage targets before implementation (test-first approach)
- Build testing infrastructure/framework first
- Use data-test attributes for stable selectors
- Create reusable test commands and utilities
- Separate API and UI tests
- Run lint and tests in pre-commit hooks

❌ **DON'T:**
- Skip unit tests (they're mandatory)
- Skip E2E tests (they're mandatory)
- Test only implementation details
- Use fragile CSS selectors
- Mock everything in E2E tests (defeats the purpose)
- Ignore coverage metrics
- Assume tests add value without measuring effectiveness

---

**Prev:** [Prompt Engineering](./05-prompt-engineering.md) | **Next:** [AI-First Workflow](./07-ai-first-workflow.md)

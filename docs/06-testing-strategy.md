# Testing Strategy

Modern testing philosophy for AI-first development.

## Core Philosophy

**E2E Tests > Component Tests > Unit Tests (Optional)**

### The Pyramid is Inverted

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

AI-first testing (top-heavy):
```
  ____________
 /            \ ← E2E (comprehensive)
/__E2E Tests__\
  /          \ ← Component (targeted)
 /────────────\
  /        \ ← Unit (optional)
 /__Optional_\
```

### Why This Works

**E2E Tests:**
- ✅ Test actual user flows
- ✅ Catch integration issues
- ✅ Verify the whole system
- ✅ Document expected behavior
- ✅ Enable confident refactoring

**Component Tests:**
- ✅ Test complex UI logic
- ✅ Faster than E2E
- ✅ Target specific behaviors
- ⚠️ Not always necessary

**Unit Tests:**
- ⚠️ Often test implementation details
- ⚠️ Break on refactoring
- ⚠️ False sense of security
- ✅ Useful for critical algorithms
- ✅ Optional for most code

## The Scientific Approach

**Unit Tests Are Optional, Not Mandatory**

Instead of assuming unit tests add value, **measure their impact:**

### A/B Test Your Testing Strategy

**Team A: E2E + Unit Tests**
- Write E2E tests for all features
- Write unit tests for all functions
- Track: bugs caught, time spent, false positives

**Team B: E2E Only**
- Write comprehensive E2E tests
- Skip unit tests unless clearly needed
- Track: bugs caught, time spent, velocity

**Measure after 3 months:**
- Which team caught more bugs?
- Which team shipped faster?
- Which team had fewer production issues?
- Which tests had the best signal-to-noise ratio?

### When to Write Unit Tests

Write unit tests ONLY when:
1. **Complex algorithms** - Math, parsing, encryption
2. **Edge cases** - Hard to reproduce in E2E
3. **Performance critical** - Need to benchmark specific functions
4. **Shared utilities** - Used across many features

**Skip unit tests for:**
- Simple CRUD operations
- Glue code
- UI components
- Database queries
- API handlers (use E2E instead)

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

## Unit Testing (Optional)

Only write unit tests when there's clear value.

### Good Use Case: Complex Algorithm

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

### Bad Use Case: Simple CRUD

```javascript
❌ // Don't write unit tests for this
class UserRepository {
  async findById(id) {
    return await db.query('SELECT * FROM users WHERE id = ?', [id])
  }
}

// This is testing the database, not your code
test('findById returns user', async () => {
  const user = await repo.findById(1)
  expect(user).toBeDefined()
})

✅ // Instead, write E2E test
test('GET /api/users/:id returns user', () => {
  cy.request('/api/users/1')
    .its('body')
    .should('have.property', 'email')
})
```

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
- ✅ No console errors
- ✅ Build succeeds
- ⚠️ Unit test coverage (optional)

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
- Write comprehensive E2E tests
- Test user journeys, not functions
- Use data-test attributes
- Create reusable commands
- Separate API and UI tests
- Only write unit tests when clearly valuable
- Measure test effectiveness

❌ **DON'T:**
- Test implementation details
- Write unit tests for everything
- Use fragile CSS selectors
- Mock everything (defeats E2E purpose)
- Skip E2E because they're "slow"
- Assume unit tests add value without measuring

---

**Prev:** [Prompt Engineering](./05-prompt-engineering.md) | **Next:** [AI-First Workflow](./07-ai-first-workflow.md)

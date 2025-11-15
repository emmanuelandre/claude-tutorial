# Prompt Engineering for Claude Code

Master the art of communicating effectively with Claude Code.

## Core Principles

### 1. Be Specific, Not Vague

❌ **Vague:**
```
"Fix the authentication"
```

✅ **Specific:**
```
"Fix the authentication bug where token refresh fails when
multiple API calls happen simultaneously, causing a race
condition. The token should be refreshed once and queued
requests should wait for the new token."
```

### 2. Provide Context

❌ **No Context:**
```
"Add a search feature"
```

✅ **With Context:**
```
"Add a search feature to the user management page that:
- Searches by name, email, and role
- Debounces input (300ms)
- Highlights matching text
- Updates URL query params
- Maintains pagination state"
```

### 3. Include Examples

❌ **Abstract:**
```
"Create an API endpoint for user preferences"
```

✅ **With Examples:**
```
"Create a PUT /api/v1/users/:id/preferences endpoint that accepts:
{
  "theme": "dark",
  "language": "en",
  "notifications": {
    "email": true,
    "push": false
  }
}

Returns 200 with updated preferences or 400 if validation fails."
```

## Prompt Patterns

### Pattern 1: Feature Request

**Template:**
```
I need to implement [FEATURE].

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Technical details:
- Use [technology/library]
- Follow [pattern/convention]
- Ensure [quality requirement]

Success criteria:
- [How to verify it works]
```

**Example:**
```
I need to implement user profile editing.

Requirements:
- Users can update their name, email, and bio
- Email must be unique and validated
- Changes are saved to database
- Show success/error messages

Technical details:
- Use React Hook Form for validation
- PUT request to /api/v1/users/:id
- Optimistic UI updates
- Handle network errors gracefully

Success criteria:
- Form validates correctly
- Database updates persist
- UI shows loading states
- Error messages are clear
```

### Pattern 2: Bug Fix

**Template:**
```
I'm experiencing [PROBLEM].

What I expect:
[Expected behavior]

What actually happens:
[Actual behavior]

Steps to reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Error message/stack trace:
[Paste error]

Relevant context:
- [Browser/environment]
- [Recent changes]
- [What I've tried]
```

**Example:**
```
I'm experiencing a 401 Unauthorized error after 1 hour.

What I expect:
Users should stay logged in indefinitely with token refresh.

What actually happens:
After 1 hour, all API calls return 401 and user is logged out.

Steps to reproduce:
1. Log in successfully
2. Wait 1 hour
3. Try to make any API call
4. Receive 401 error

Error message:
{
  "error": "Token expired",
  "code": "AUTH_EXPIRED"
}

Relevant context:
- Token expiry is set to 1 hour in JWT config
- Refresh token endpoint exists but isn't being called
- This started after upgrading axios to v1.6
```

### Pattern 3: Refactoring

**Template:**
```
I want to refactor [CODE/COMPONENT] to [GOAL].

Current implementation:
[Describe current state]

Desired outcome:
[Describe target state]

Constraints:
- [Constraint 1]
- [Constraint 2]

Requirements:
- [Requirement 1]
- [Requirement 2]
```

**Example:**
```
I want to refactor the authentication middleware to support
multiple auth providers (Google, GitHub, Email).

Current implementation:
- Single Google OAuth flow hardcoded
- Middleware only checks for Google tokens
- User creation logic mixed with auth logic

Desired outcome:
- Strategy pattern for auth providers
- Pluggable provider system
- Separated concerns (auth vs user management)

Constraints:
- Must not break existing Google OAuth
- Database schema can change (via migration)
- Frontend routes can change if needed

Requirements:
- All existing tests must pass
- Add tests for new providers
- Update documentation
```

### Pattern 4: Multi-Step Task

**Template:**
```
I need to implement [FEATURE]. Please:

1. [Step 1 with details]
2. [Step 2 with details]
3. [Step 3 with details]
4. [Step 4 with details]

After each step:
- [Validation requirement]
```

**Example:**
```
I need to implement analytics dashboard. Please:

1. Create database table for analytics events
   - Columns: id, user_id, event_type, metadata (jsonb), timestamp
   - Add indexes on user_id and timestamp

2. Add analytics tracking to API
   - Middleware that logs all requests
   - Function to track custom events
   - Batch insert every 100 events or 10 seconds

3. Create analytics API endpoints
   - GET /api/v1/analytics/users/:id - user-specific stats
   - GET /api/v1/analytics/summary - overall metrics
   - Both with date range filters

4. Build React dashboard component
   - Charts using recharts library
   - Real-time updates every 30 seconds
   - Export to CSV functionality

After each step:
- Run tests and ensure they pass
- Verify in browser/API client
```

## Advanced Techniques

### Chain of Thought

Instead of asking for the final solution, guide Claude through reasoning:

```
"Before implementing the caching layer, help me think through:

1. What data should we cache?
   - Analyze current API call patterns
   - Identify frequently requested, rarely changing data

2. What cache invalidation strategy makes sense?
   - Consider our update frequency
   - Evaluate TTL vs event-based invalidation

3. Where should the cache live?
   - Compare Redis, in-memory, CDN options
   - Consider our scale and infrastructure

Based on this analysis, recommend and implement a solution."
```

### Iterative Refinement

Start broad, then refine:

```
Session 1: "Create a basic user registration flow"
Session 2: "Add email verification to registration"
Session 3: "Add password strength requirements"
Session 4: "Add rate limiting to prevent abuse"
Session 5: "Add admin approval workflow"
```

### Specification-Driven

Provide a detailed spec first:

```
"Here's the API specification for the new feature:

[Paste OpenAPI/Swagger spec or detailed API contract]

Please implement:
1. Database schema and migration
2. Repository layer with these exact method signatures
3. API handlers matching the spec
4. Unit tests for repository
5. E2E tests for API endpoints"
```

## Communication Best Practices

### Do's

✅ **Reference file paths:**
```
"In src/components/UserProfile.jsx, update the avatar upload
function to use the new /api/v1/upload endpoint"
```

✅ **Paste relevant code:**
```
"This function is failing:
```javascript
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}
```
It doesn't handle errors. Please add proper error handling."
```

✅ **Specify technologies:**
```
"Use React Query for data fetching, not plain fetch"
"Use Zod for validation, not Joi"
```

✅ **Define success:**
```
"This is done when:
- All E2E tests pass
- No console errors
- Works in Chrome, Firefox, Safari
- Loading states are smooth"
```

### Don'ts

❌ **Assume context:**
```
"Fix the bug" (Which bug? Where?)
```

❌ **Be ambiguous:**
```
"Make it better" (Better how?)
```

❌ **Omit constraints:**
```
"Add caching" (What tech? What TTL? Where?)
```

❌ **Skip verification steps:**
```
"Just implement it" (No test requirements?)
```

## Project-Specific Prompts

### For New Features

```
"Implement [FEATURE] following our project standards:

Check CLAUDE.md for:
- Code structure conventions
- Testing requirements
- Commit message format
- Required pre-commit checks

Ensure:
- Follows existing patterns in [similar feature]
- Maintains consistency with [related code]
- Updates relevant documentation
- Includes comprehensive tests"
```

### For Debugging

```
"I'm debugging [ISSUE].

Please:
1. Analyze the code in [file/directory]
2. Check logs/errors for clues
3. Identify the root cause
4. Propose a fix
5. Explain why this happened
6. Suggest how to prevent similar issues

Do NOT just fix it - help me understand it."
```

### For Code Review

```
"Review the changes in [branch/PR].

Focus on:
- Correctness and logic errors
- Performance implications
- Security vulnerabilities
- Code style and conventions
- Test coverage gaps
- Documentation updates needed

Provide specific feedback with file:line references."
```

## Common Mistakes

### Mistake 1: Over-Reliance

❌ **Wrong:**
```
"Build me a complete e-commerce platform"
```

✅ **Right:**
```
"Let's build an e-commerce platform step by step.

First, help me design the database schema for:
- Products
- Users
- Orders
- Inventory

Then we'll implement features one at a time, starting with
product catalog."
```

### Mistake 2: Under-Specification

❌ **Wrong:**
```
"Add validation"
```

✅ **Right:**
```
"Add validation to the registration form:
- Email: valid format, check if already exists
- Password: min 8 chars, must have uppercase, number, symbol
- Username: 3-20 chars, alphanumeric only, check uniqueness
- Show inline error messages on blur"
```

### Mistake 3: Forgetting Tests

❌ **Wrong:**
```
"Implement user authentication"
```

✅ **Right:**
```
"Implement user authentication with comprehensive E2E tests covering:
- Successful login
- Wrong password
- Non-existent user
- Account locked
- Token refresh
- Logout
All tests must pass before considering this complete."
```

## Tips

1. **Start sessions with context:**
   ```
   "Continuing work on the analytics dashboard.
    Last session we implemented the data collection layer.
    Today we're building the visualization components."
   ```

2. **Use checkpoints:**
   ```
   "Implement the feature in stages. After each stage,
    commit the changes so we can roll back if needed."
   ```

3. **Request explanations:**
   ```
   "Implement the solution, but also explain:
    - Why this approach?
    - What are the trade-offs?
    - What could go wrong?"
   ```

4. **Verify understanding:**
   ```
   "Before implementing, confirm you understand:
    - The goal is [X]
    - The constraints are [Y]
    - Success looks like [Z]
    Is this correct?"
   ```

---

**Prev:** [The CLAUDE.md File](./04-claude-md.md) | **Next:** [Testing Strategy](./06-testing-strategy.md)

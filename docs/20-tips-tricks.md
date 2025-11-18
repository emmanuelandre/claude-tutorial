# Tips & Tricks for Claude Code

Power user techniques for maximum productivity.

## Communication

### Be Specific
❌ "Fix the bug"
✅ "Fix the race condition in token refresh where concurrent requests cause duplicate tokens"

### Provide Context
❌ "Update the login"
✅ "Update the login form to add remember me checkbox, storing preference in localStorage for 30 days"

### Reference Files
❌ "Change the user model"
✅ "In src/models/user.ts, add email_verified boolean field and update the User type"

## Project Organization

### Keep CLAUDE.md Updated
```bash
# After any significant change
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with new patterns"
```

### Document Sessions
Create session logs to track progress:
```
project/sessions/2024-11-15_auth-implementation.md
```

### Use Templates
Keep reusable templates for:
- API endpoints
- Database models
- Test files
- Component structure

## Productivity Hacks

### Multi-Step Requests
```
"I need to implement user preferences. Please:
1. Create database migration for preferences table
2. Add repository methods
3. Create API endpoints (CRUD)
4. Write E2E tests
5. Update OpenAPI spec"
```

### Batch Related Changes
```
"Update all API error responses to use consistent format:
{ error: string, code: string, details?: object }"
```

### Progressive Refinement
```
1. "Create basic user registration"
2. "Add email verification"
3. "Add password strength requirements"
4. "Add rate limiting"
```

## Working with Large Codebases

### Navigate Efficiently
```
"Show me all files that handle authentication"
"Find where JWT tokens are generated"
"List all API endpoints related to users"
```

### Understand Before Changing
```
"Explain how the current auth flow works"
"What are the dependencies of the UserService?"
"Why is this caching mechanism used here?"
```

### Refactor Safely
```
"Refactor the auth middleware to support multiple providers.
Ensure all existing tests still pass."
```

## Testing Strategies

### Request Comprehensive Tests
```
"Generate E2E tests covering:
- Happy path
- Invalid inputs
- Permission errors
- Rate limiting
- Edge cases"
```

### Test-Driven Requests
```
"First write E2E tests for the checkout flow,
then implement the feature to make tests pass"
```

## Debugging

### Systematic Approach
```
"I'm getting 'undefined is not a function' in checkout.
The error occurs after payment submission.
Here's the stack trace: [paste trace]
Help me debug this."
```

### Reproduce Issues
```
"Create a minimal reproduction of the CORS error:
1. Frontend on localhost:3000
2. API on localhost:8080
3. Fetch request fails with CORS"
```

## Performance

### Profile Before Optimizing
```
"The /users endpoint is slow (>2s).
Profile the database queries and suggest optimizations."
```

### Request Benchmarks
```
"Add benchmarks for the search functionality
and identify bottlenecks"
```

## Security

### Security Review Requests
```
"Review the authentication code for security issues:
- SQL injection
- XSS vulnerabilities
- Token security
- Rate limiting
- Input validation"
```

### Secure by Default
```
"Implement password reset with security best practices:
- Time-limited tokens
- One-time use
- Rate limiting
- Audit logging"
```

## Documentation

### Auto-Generate Docs
```
"Generate API documentation from the OpenAPI spec
in Markdown format for the README"
```

### Keep README Current
```
"Update README.md with:
- New environment variables
- Updated setup steps
- Recent features added"
```

## Version Control

### Meaningful Commits
```
# Before committing
"Review my changes and suggest appropriate commit messages
following conventional commits format"
```

### PR Descriptions
```
"Generate a detailed PR description for these changes
including summary, testing notes, and breaking changes"
```

## Advanced Techniques

### Code Generation from Specs
```
"From this OpenAPI spec, generate:
- TypeScript types
- API client
- Mock server
- E2E tests"
```

### Polyglot Development
```
"Port this Python function to Go:
[paste function]
Maintain the same behavior and add tests"
```

### Architectural Reviews
```
"Review this microservice architecture for:
- Scalability issues
- Single points of failure
- Performance bottlenecks
- Security concerns"
```

## Time-Saving Shortcuts

### Boilerplate Generation
```
"Create boilerplate for a new API endpoint:
- Handler
- Repository method
- Validation
- Tests
- OpenAPI entry"
```

### Migration Scripts
```
"Generate migration script to:
1. Add new column
2. Migrate existing data
3. Add constraints
4. Verify data integrity"
```

### Config Files
```
"Generate complete setup for:
- ESLint
- Prettier
- TypeScript
- Jest
Following current project conventions"
```

## Collaboration

### Onboarding New Developers
```
"Create an onboarding guide covering:
- Setup steps
- Architecture overview
- Development workflow
- Common tasks
- Where to find things"
```

### Knowledge Transfer
```
"Document the payment processing flow with:
- Sequence diagram
- Key components
- Error handling
- Testing approach"
```

## Continuous Improvement

### Regular Reviews
```
"Analyze last month's commits and suggest:
- Code patterns to standardize
- Repeated bugs to prevent
- Documentation gaps to fill"
```

### Metrics Tracking
```
"Generate monthly development metrics:
- Features delivered
- Bugs fixed
- Test coverage changes
- PR cycle time"
```

## Common Mistakes to Avoid

❌ Vague requests
❌ Skipping context
❌ Not reviewing AI output
❌ Committing untested code
❌ Ignoring CLAUDE.md
❌ Large, unfocused PRs
❌ Letting AI merge PRs

✅ Specific requests
✅ Full context provided
✅ Always review & test
✅ Tests before commit
✅ Keep CLAUDE.md current
✅ Small, focused changes
✅ Human-only merges

## Pro Tips

1. **Start sessions with context**: "Working on auth feature, current progress: [summary]"
2. **End sessions with notes**: Document what was done and next steps
3. **Use checkpoints**: Commit after each logical step
4. **Leverage history**: Reference previous sessions
5. **Iterate quickly**: Start working, refine as you go
6. **Trust but verify**: Review AI output always
7. **Learn patterns**: Note what prompts work best
8. **Share knowledge**: Document learnings for team

---

**Prev:** [Troubleshooting](./19-troubleshooting.md) | **Next:** [Resources](./21-resources.md)

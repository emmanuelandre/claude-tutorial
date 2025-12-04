# Advanced Topics

Advanced techniques for experienced Claude Code users.

## MCP (Model Context Protocol) Servers

MCP servers extend Claude Code's capabilities with custom tools.

### What Are MCP Servers?

MCP servers provide:
- Custom tools for specific domains (databases, APIs, services)
- Access to local resources (files, processes)
- Integration with external services
- Specialized functionality beyond built-in tools

### Common MCP Servers

| Server | Purpose | Use Case |
|--------|---------|----------|
| filesystem | File operations | Read/write files outside workspace |
| postgres | Database queries | Direct database access |
| github | GitHub API | PR management, issues |
| slack | Messaging | Team notifications |
| puppeteer | Browser automation | Web scraping, testing |

### Setting Up MCP Servers

**Configuration file:**
```json
// ~/.claude/mcp_servers.json
{
  "servers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "postgres://user:pass@localhost:5432/db"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_PATHS": "/home/user/projects,/tmp"
      }
    }
  }
}
```

### Creating Custom MCP Servers

**Basic structure (TypeScript):**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-custom-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});

// Define a tool
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "my_tool",
    description: "Does something useful",
    inputSchema: {
      type: "object",
      properties: {
        param: { type: "string", description: "Input parameter" }
      },
      required: ["param"]
    }
  }]
}));

// Handle tool calls
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "my_tool") {
    const result = await doSomething(request.params.arguments.param);
    return { content: [{ type: "text", text: result }] };
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Using your custom server:**
```
// Tell Claude to use your MCP tool
Use the my_tool to process "input data"
```

---

## Multi-Repository Projects

Managing multiple repositories with Claude Code.

### Workspace Setup

**VS Code multi-root workspace:**
```json
// project.code-workspace
{
  "folders": [
    { "path": "service-api" },
    { "path": "service-web" },
    { "path": "service-worker" },
    { "path": "infrastructure" }
  ],
  "settings": {
    "files.exclude": {
      "**/node_modules": true
    }
  }
}
```

### Cross-Repo Context

**Share context with Claude:**
```
I'm working on a microservices project with multiple repos:

1. service-api/ - Go REST API
   - CLAUDE.md defines API conventions
   - Endpoints in internal/handlers/

2. service-web/ - React frontend
   - CLAUDE.md defines component patterns
   - API client in src/api/

3. infrastructure/ - Docker, Kubernetes
   - CLAUDE.md defines deployment patterns
   - Shared types in proto/

When making changes, ensure consistency across repos.
Current task: Add a new "orders" endpoint...
```

### Shared Types Between Services

**Protocol Buffers for shared types:**
```protobuf
// proto/order.proto
syntax = "proto3";

message Order {
  int64 id = 1;
  int64 user_id = 2;
  repeated OrderItem items = 3;
  string status = 4;
  double total = 5;
}

message OrderItem {
  int64 product_id = 1;
  int32 quantity = 2;
  double price = 3;
}
```

**Generate for each language:**
```bash
# Go
protoc --go_out=service-api/pkg/proto order.proto

# TypeScript
protoc --ts_out=service-web/src/proto order.proto
```

### Coordinated Changes

**Multi-repo PR workflow:**
```
Making a change that affects multiple repos:

1. API changes (service-api)
   - New endpoint: POST /api/orders
   - PR: api-repo#123

2. Frontend changes (service-web)
   - New OrderForm component
   - API client update
   - PR: web-repo#456

3. Infrastructure changes (infrastructure)
   - Update API deployment
   - PR: infra-repo#789

Merge order: API → Infrastructure → Frontend
```

---

## Advanced CLAUDE.md Patterns

### Context Optimization

**Structured sections for large projects:**
```markdown
# CLAUDE.md

## Quick Reference
[Most frequently needed info - always read this]

## Architecture Overview
[High-level system design]

## Current Sprint Context
[What we're working on now - update weekly]

## Deep Dive Sections
### Database Schema
[Link to separate file: docs/database.md]

### API Reference
[Link to separate file: docs/api.md]

## Historical Decisions
[Link to ADR folder: docs/adr/]
```

### Project-Specific Commands

**Define common workflows:**
```markdown
## Common Prompts

### Adding a New API Endpoint
```
Add a new endpoint for [resource]:
1. Create migration in migrations/
2. Add repository methods in internal/repository/
3. Create handler in internal/handlers/
4. Add routes in cmd/server/routes.go
5. Write E2E tests in tests/e2e/
6. Update API documentation

Follow existing patterns from the users endpoint.
```

### Debugging a Test Failure
```
Debug the failing test:
1. Read the test file
2. Identify the assertion that fails
3. Check the handler/repository being tested
4. Add debug logging if needed
5. Fix the issue
6. Verify all tests pass
```
```

### Dynamic Context

**Include current state:**
```markdown
## Current Development State

**Last Updated:** 2025-01-15

### In Progress
- Feature: Order management (branch: feature/orders)
- Blocked: Waiting for payment gateway access

### Recently Completed
- User authentication (merged: 2025-01-10)
- Product catalog (merged: 2025-01-12)

### Known Issues
- Performance issue on /api/products with large datasets (#123)
- Flaky test in auth_test.go (#124)
```

---

## Complex Refactoring

### Large-Scale Codebase Changes

**Incremental migration strategy:**
```
We need to migrate from REST to GraphQL. Plan:

Phase 1: Add GraphQL alongside REST
- Set up GraphQL server
- Create schemas for existing models
- Add resolvers that call existing services
- Both REST and GraphQL work

Phase 2: Migrate high-traffic endpoints
- Orders API → GraphQL
- Products API → GraphQL
- Update frontend to use GraphQL for these

Phase 3: Migrate remaining endpoints
- Users API → GraphQL
- Admin API → GraphQL

Phase 4: Deprecate REST
- Add deprecation warnings
- Set sunset date
- Remove REST endpoints

Each phase is a separate PR. Tests must pass at each phase.
```

### Maintaining Tests During Refactoring

```
Refactoring the repository layer:

Rules:
1. Tests must pass before AND after each change
2. Run tests after every file change
3. If tests fail, fix before continuing
4. Don't change tests and implementation in same commit

Process:
1. Create new implementation alongside old
2. Add tests for new implementation
3. Migrate callers one at a time
4. Remove old implementation when unused
5. Clean up

Current step: [specify which step]
```

### Safe Renaming

```
Rename UserService to AccountService across codebase:

Steps:
1. Create AccountService as alias to UserService
2. Update all imports to use AccountService
3. Run tests - must pass
4. Update internal implementation
5. Remove UserService alias
6. Update documentation

Do NOT:
- Rename and update usages in same commit
- Skip test runs between steps
- Update tests before implementation
```

---

## Working with Legacy Code

### Understanding Undocumented Code

```
I need to understand this legacy code:

File: src/legacy/processor.go

Please:
1. Read the file and all related files it imports
2. Trace the data flow from input to output
3. Identify side effects (database, external APIs)
4. Document assumptions and magic numbers
5. Create a summary of what this code does

Don't modify anything yet - just document.
```

### Adding Tests to Legacy Code

```
Add tests to legacy code without modifying it:

File: src/legacy/calculator.go

Approach:
1. Read and understand the code
2. Identify public functions to test
3. Create test file: calculator_test.go
4. Write tests for current behavior (not ideal behavior)
5. Tests should pass with existing code
6. Document any bugs found (don't fix yet)

Goal: Establish a safety net before refactoring.
```

### Incremental Modernization

```
Modernize legacy authentication module:

Current state:
- Uses deprecated crypto library
- No tests
- Mixed concerns (auth + session + user)

Target state:
- Modern crypto (bcrypt)
- 80% test coverage
- Separated concerns

Plan:
Phase 1: Add tests for current behavior
Phase 2: Extract session management
Phase 3: Extract user management
Phase 4: Update crypto library
Phase 5: Add integration tests

We're on Phase 1. Add tests without changing code.
```

---

## Context Window Optimization

### Managing Large Codebases

**Strategies for staying within context limits:**

1. **Reference, don't repeat:**
```
See the pattern in src/handlers/users.go lines 50-80.
Apply the same pattern to the new orders handler.
```

2. **Summarize large files:**
```
The database schema has 30 tables. Relevant ones for this task:
- users (id, email, password_hash)
- orders (id, user_id, total, status)
- order_items (id, order_id, product_id, quantity)
```

3. **Focus on diff:**
```
Only these files need changes:
1. src/handlers/orders.go - Add CreateOrder handler
2. src/repository/orders.go - Add Create method
3. tests/orders_test.go - Add tests

Other files are stable - don't read unless needed.
```

### Efficient File Reading

```
Read only what's needed:

For this task (adding order validation):
1. Read: src/handlers/orders.go (need to see current handler)
2. Read: src/validation/rules.go (need existing patterns)
3. Skip: src/repository/* (not changing data layer)
4. Skip: tests/* (will update after implementation)

Start with handlers/orders.go
```

---

## Extending Claude Code

### Custom Slash Commands

Create project-specific commands:

```markdown
<!-- .claude/commands/new-endpoint.md -->
# New Endpoint Command

Create a new API endpoint with:
- Handler in internal/handlers/
- Repository method in internal/repository/
- Migration if needed
- E2E tests in tests/e2e/
- Unit tests for business logic

Arguments:
- $RESOURCE: The resource name (e.g., "orders")
- $METHODS: HTTP methods to support (e.g., "GET,POST,PUT,DELETE")

Follow patterns from existing endpoints.
Start with the database migration.
```

**Usage:**
```
/project:new-endpoint orders GET,POST,PUT,DELETE
```

### Automation Scripts

**Git hooks integration:**
```bash
#!/bin/bash
# .git/hooks/prepare-commit-msg

# Auto-generate commit message suggestion
if [ -z "$2" ]; then
  # Get changed files
  FILES=$(git diff --cached --name-only)

  # Create prompt for Claude
  echo "Based on these changed files, suggest a commit message:" > /tmp/commit-prompt
  echo "$FILES" >> /tmp/commit-prompt
  git diff --cached >> /tmp/commit-prompt

  # Could integrate with Claude API here
  # For now, just remind the developer
  echo "# Changed files:" >> "$1"
  echo "$FILES" | sed 's/^/# /' >> "$1"
fi
```

### Integration with Other Tools

**VS Code tasks:**
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Tests for Current File",
      "type": "shell",
      "command": "go test -v ./${relativeFileDirname}/...",
      "group": "test",
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "Generate Mocks",
      "type": "shell",
      "command": "mockgen -source=${relativeFile} -destination=mocks/${fileBasenameNoExtension}_mock.go",
      "group": "build"
    }
  ]
}
```

---

## Summary

**Key Advanced Techniques:**
- MCP servers extend Claude's capabilities
- Multi-repo projects need coordinated context
- CLAUDE.md can include dynamic state
- Refactoring requires incremental, tested steps
- Legacy code needs tests before changes
- Optimize context usage for large codebases

**When to Use Advanced Techniques:**
- Project complexity exceeds basic patterns
- Standard approaches don't fit your needs
- Performance or scale requires optimization
- Legacy systems need careful handling

---

**Prev:** [CI/CD and Deployment](./17-ci-cd.md) | **Next:** [Troubleshooting](./19-troubleshooting.md)

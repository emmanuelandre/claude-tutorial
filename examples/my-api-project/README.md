# my-api-project Reference Example

This is a reference implementation for the Claude Code workshop exercises (Pages 9-19).

## Purpose

This example shows what a completed Go API project looks like after following the workshop exercises. Use it to:

- **Compare** your generated CLAUDE.md against a production-ready version
- **Reference** proper migration structure with up/down files
- **Understand** trigger patterns for automatic timestamp updates

> **Important:** This is a reference for comparison, not copy-paste. Complete the exercises yourself first, then compare your output.

## What's Included

```
my-api-project/
├── README.md                     # This file
├── CLAUDE.md                     # Complete project configuration
└── migrations/
    ├── 001_create_users.up.sql   # User table creation
    └── 001_create_users.down.sql # Rollback migration
```

## How to Use

### During Workshop

1. Complete each exercise independently
2. After finishing, compare your output to these files
3. Note differences - different approaches are OK if they work!

### After Workshop

- Use as a template for starting new Go API projects
- Reference the patterns used (indexes, triggers, conventions)
- Adapt the CLAUDE.md structure for your own projects

## Key Patterns Demonstrated

### CLAUDE.md

- Project overview and architecture
- Tech stack with specific versions (Go 1.21+, PostgreSQL 16)
- Git workflow conventions matching workshop teachings
- Testing strategy with coverage targets
- Environment configuration
- Pre-commit checklist

### Database Migration

- Serial primary key pattern
- Email uniqueness constraint with index
- Automatic `updated_at` trigger
- Proper up/down migration pair for rollback support
- Index on frequently-queried columns

## Workshop Exercise Reference

| Workshop Page | This Example |
|---------------|--------------|
| Page 9: Create CLAUDE.md | See `CLAUDE.md` |
| Page 14-15: Database Schema | See `migrations/001_create_users.up.sql` |

## Note

This is a minimal example focused on the workshop exercises. For a comprehensive CLAUDE.md template covering all aspects of a production project, see [`../claude-md-template.md`](../claude-md-template.md).

## Related Documentation

- [Documentation Organization](../../docs/12-documentation-organization.md) - How to structure project documentation
- [Git Workflow](../../docs/11-git-workflow.md) - Branch and commit conventions
- [Testing Strategy](../../docs/06-testing-strategy.md) - E2E and unit testing approach

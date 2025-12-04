# Documentation Organization

How to structure your project documentation for effective AI-first development.

## Why Documentation Structure Matters

In AI-first development, your documentation serves multiple purposes:
- **Context for Claude** - Persistent knowledge across sessions
- **Team alignment** - Single source of truth for conventions
- **Progress tracking** - Clear visibility into project state
- **Knowledge preservation** - Decisions and rationale captured

The right structure depends on your project size, team, and duration.

## The Two Patterns

### Pattern 1: Simple Flat Structure

Best for: Solo projects, < 20 tasks, short duration (weeks)

```
project-root/
├── CLAUDE.md              # Project configuration for Claude
├── README.md              # Project overview
├── plan.md                # Development roadmap
├── architecture.md        # System design
├── requirements.md        # Feature requirements
├── ui-specs.md            # UI specifications (if applicable)
└── src/                   # Source code
```

**Advantages:**
- Quick to set up
- Easy to navigate
- Low overhead
- All context in one place

**When to use:**
- Solo developer or pair
- Project duration < 1 month
- Single service/application
- < 20 total tasks

### Pattern 2: Nested Directory Structure

Best for: Teams, 20+ tasks, long-term projects

```
project-root/
├── CLAUDE.md              # Project configuration
├── README.md              # Project overview
├── project/               # Documentation hub
│   ├── planning/          # Master plans and progress
│   │   ├── devplan.md
│   │   ├── devprogress.md
│   │   ├── database.md
│   │   └── sitemap.md
│   ├── specs/             # Feature specifications
│   │   ├── 01-auth.md
│   │   ├── 02-dashboard.md
│   │   └── ...
│   ├── architecture/      # Architecture documents
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   └── infrastructure.md
│   ├── sessions/          # Session summaries
│   └── archive/           # Historical docs
└── src/
```

**Advantages:**
- Scales with project complexity
- Clear separation of concerns
- Better for team collaboration
- Supports phased development

**When to use:**
- Team of 2+ developers
- Project duration > 1 month
- Multiple services/components
- 20+ tasks across phases

> See [Project Planning & Documentation Structure](./09-project-planning-structure.md) for detailed guidance on the nested pattern.

## Decision Matrix

| Factor | Flat Structure | Nested Structure |
|--------|---------------|------------------|
| Team size | 1-2 developers | 3+ developers |
| Project duration | < 1 month | > 1 month |
| Task count | < 20 tasks | 20+ tasks |
| Services | Single service | Multiple services |
| Phases | 1-2 phases | 3+ phases |

**Decision flowchart:**

```
Is your project > 1 month duration?
├── No → Use Flat Structure
└── Yes → Do you have 20+ tasks?
    ├── No → Use Flat Structure
    └── Yes → Use Nested Structure
```

---

## Core Documentation Files

These files are essential regardless of which pattern you choose.

### plan.md / devplan.md

**Purpose:** Development roadmap, task tracking, and progress visibility.

**Template (Flat Pattern):**

```markdown
# Development Plan

## Overview
[One-paragraph project description]

## Goals
- [ ] Goal 1: [Description]
- [ ] Goal 2: [Description]
- [ ] Goal 3: [Description]

## Milestones

### Milestone 1: [Name]
**Target:** [Date or sprint]
**Status:** In Progress / Complete / Blocked

Tasks:
- [ ] Task 1.1: [Description]
- [ ] Task 1.2: [Description]
- [x] Task 1.3: [Completed task]

### Milestone 2: [Name]
**Target:** [Date or sprint]
**Status:** Not Started

Tasks:
- [ ] Task 2.1: [Description]
- [ ] Task 2.2: [Description]

## Current Focus

**Active:** [Current task being worked on]
**Next:** [Next task after current]
**Blocked:** [Any blockers, or "None"]

## Completed

- [x] [Completed milestone or task]
- [x] [Completed milestone or task]

## Notes

[Any important context, decisions, or changes to the plan]
```

**Template (Nested Pattern - devplan.md):**

```markdown
# Project Development Plan

## Development Strategy

### Core Principles
1. Database First - Schema before implementation
2. API First - Backend before frontend
3. Test Driven - Tests at each layer
4. Incremental - Follow dependency order
5. Vertical Slices - Complete stack per feature

### Implementation Workflow (Per Feature)
1. DATABASE: Migration → Repository → Mock data
2. BACKEND API: Handlers → Validation → Permissions
3. API E2E TESTS: Cypress/Playwright tests → All pass
4. FRONTEND UI: Components → Forms → Integration
5. UI E2E TESTS: UI tests → All pass
6. DOCUMENTATION: API docs → Comments → Changelog

### Dependency Map
```
[Entity] → [Entity] → [Entity]
Example: Organizations → Users → Permissions → Features
```

### Development Phases

#### Phase 0: Foundation
- [ ] Database setup
- [ ] Authentication
- [ ] Core infrastructure

#### Phase 1: Core Features
- [ ] Feature A
- [ ] Feature B

#### Phase 2: Advanced Features
- [ ] Feature C
- [ ] Feature D

[Continue for all phases...]
```

---

### architecture.md

**Purpose:** System design, component relationships, and technical decisions.

**Template:**

```markdown
# Architecture

## System Overview

[High-level description of what the system does and its main components]

## Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │────▶│  Database   │
│  (React)    │     │   (Go)      │     │ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Cache     │
                    │  (Redis)    │
                    └─────────────┘
```

## Components

### Component: [Name]
**Purpose:** [What it does]
**Technology:** [Tech stack]
**Key Files:**
- `path/to/main/file`
- `path/to/other/file`

**Responsibilities:**
- Responsibility 1
- Responsibility 2

### Component: [Name]
[Repeat for each component...]

## Data Flow

### Flow: [User Action]
1. User initiates [action]
2. Frontend sends request to [endpoint]
3. API validates and processes
4. Database updated
5. Response returned

## Key Architectural Decisions

| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| Database | PostgreSQL, MySQL, MongoDB | PostgreSQL | ACID compliance, JSON support |
| Auth | Sessions, JWT | JWT | Stateless, mobile-friendly |
| Cache | Redis, Memcached | Redis | Data structures, persistence |

## External Dependencies

| Dependency | Purpose | Documentation |
|------------|---------|---------------|
| Stripe | Payments | [Link] |
| SendGrid | Email | [Link] |

## Security Considerations

- All API endpoints require authentication except [exceptions]
- Sensitive data encrypted at rest
- HTTPS enforced in production
```

---

### requirements.md

**Purpose:** Functional and non-functional requirements with acceptance criteria.

**Template:**

```markdown
# Requirements

## Functional Requirements

### FR-001: [Feature Name]
**Priority:** High / Medium / Low
**Status:** Planned / In Progress / Complete

**Description:**
[What the feature does from user perspective]

**User Story:**
As a [role], I want to [action] so that [benefit].

**Acceptance Criteria:**
- [ ] Criterion 1: [Specific, testable condition]
- [ ] Criterion 2: [Specific, testable condition]
- [ ] Criterion 3: [Specific, testable condition]

**Dependencies:**
- FR-XXX: [Dependent feature]

---

### FR-002: [Feature Name]
[Repeat structure...]

---

## Non-Functional Requirements

### NFR-001: Performance
- Page load time < 3 seconds on 3G
- API response time < 500ms (p95)
- Support 1000 concurrent users

### NFR-002: Security
- OWASP Top 10 compliance
- Data encrypted at rest and in transit
- Session timeout after 30 minutes inactivity

### NFR-003: Availability
- 99.9% uptime SLA
- Automated failover
- Daily backups with 30-day retention

### NFR-004: Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatible

## Constraints

- Must integrate with existing [system]
- Budget: [amount]
- Timeline: [deadline]
- Tech stack: [required technologies]
```

---

### ui-specs.md

**Purpose:** Frontend specifications, design system, and page layouts.

**Template:**

```markdown
# UI Specifications

## Design System

### Colors
| Name | Hex | Usage |
|------|-----|-------|
| Primary | #3B82F6 | Buttons, links, accents |
| Secondary | #6B7280 | Secondary text, borders |
| Success | #10B981 | Success states |
| Error | #EF4444 | Error states |
| Background | #F9FAFB | Page background |

### Typography
| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Inter | 36px | 700 |
| H2 | Inter | 24px | 600 |
| Body | Inter | 16px | 400 |
| Small | Inter | 14px | 400 |

### Spacing
- Base unit: 4px
- Scale: 4, 8, 12, 16, 24, 32, 48, 64

### Components
- Buttons: Primary, Secondary, Ghost, Danger
- Inputs: Text, Select, Checkbox, Radio
- Cards: Default, Elevated, Interactive

---

## Pages

### Page: [Page Name]
**Route:** `/path`
**Access:** Public / Authenticated / Admin

**Purpose:**
[What users accomplish on this page]

**Layout:**
```
┌─────────────────────────────────┐
│           Header                │
├─────────┬───────────────────────┤
│ Sidebar │      Main Content     │
│         │  ┌─────────────────┐  │
│         │  │   Component A   │  │
│         │  └─────────────────┘  │
│         │  ┌─────────────────┐  │
│         │  │   Component B   │  │
│         │  └─────────────────┘  │
└─────────┴───────────────────────┘
```

**Components:**
| Component | Purpose | Data Source |
|-----------|---------|-------------|
| Header | Navigation | Auth state |
| Sidebar | Menu items | User role |
| Component A | [Purpose] | API: /endpoint |

**States:**
- **Loading:** Skeleton placeholder
- **Empty:** "No items found" message with CTA
- **Error:** Error message with retry button
- **Success:** Data displayed in table/list

**User Actions:**
| Action | Trigger | Result |
|--------|---------|--------|
| Create item | Click "Add" button | Modal opens |
| Delete item | Click trash icon | Confirmation dialog |
| Filter | Select dropdown | List filters |

---

### Page: [Next Page]
[Repeat structure...]

---

## User Flows

### Flow: [Flow Name]
1. User lands on [page]
2. User clicks [element]
3. System displays [response]
4. User completes [action]
5. System confirms [result]

## Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | < 640px | Single column, hamburger menu |
| Tablet | 640-1024px | Two columns, collapsible sidebar |
| Desktop | > 1024px | Full layout with fixed sidebar |
```

---

### README.md

**Purpose:** Project entry point for developers and stakeholders.

**Template:**

```markdown
# Project Name

[One-line description of what this project does]

## Overview

[2-3 paragraph description covering:]
- What problem it solves
- Who it's for
- Key features

## Quick Start

### Prerequisites
- Node.js 18+
- PostgreSQL 16
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone [repo-url]
cd [project-name]

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your values

# Run database migrations
npm run db:migrate

# Start development server
npm run dev
```

### Verify Installation
```bash
# Run tests
npm test

# Open in browser
open http://localhost:3000
```

## Project Structure

```
├── src/
│   ├── api/           # API routes and handlers
│   ├── components/    # React components
│   ├── lib/           # Shared utilities
│   └── pages/         # Page components
├── tests/             # Test files
├── docs/              # Documentation
└── scripts/           # Build and utility scripts
```

## Documentation

- [Architecture](./architecture.md)
- [API Documentation](./docs/api.md)
- [Contributing Guide](./CONTRIBUTING.md)

## Development

### Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm test` | Run tests |
| `npm run lint` | Run linter |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | Secret for JWT signing | Yes |
| `PORT` | Server port (default: 3000) | No |

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `npm test`
4. Submit a pull request

## License

[License type] - see [LICENSE](./LICENSE) for details
```

---

### Rules & Memory

For persistent context across Claude sessions, use these patterns:

#### .claude/rules/ Directory

Create project-specific rules that Claude follows:

```
.claude/
└── rules/
    ├── coding-standards.md
    ├── testing-requirements.md
    └── git-conventions.md
```

**Example: coding-standards.md**
```markdown
# Coding Standards

## Naming Conventions
- Functions: camelCase
- Components: PascalCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case

## Code Organization
- One component per file
- Group related files in feature folders
- Keep files under 300 lines

## Required Patterns
- All API calls through service layer
- Error boundaries around async operations
- Loading states for all data fetching
```

#### Memory/Context Files

For session continuity, maintain context files:

**CONTEXT.md** (Session handoff)
```markdown
# Current Context

## Last Session
**Date:** 2025-01-15
**Focus:** Implementing user authentication
**Branch:** feature/user-auth

## Current State
- [x] Database migration complete
- [x] Repository layer done
- [ ] API handlers in progress (2/4 done)
- [ ] Tests not started

## Next Steps
1. Complete login handler
2. Add JWT middleware
3. Write E2E tests

## Open Questions
- Should we implement refresh tokens? (Decided: Yes)
- Token expiry time? (Pending decision)

## References
- Spec: project/specs/01-auth.md
- Migration: migrations/001_users.up.sql
```

---

## The Hybrid Approach

Start simple, evolve as needed.

### Starting Flat

Begin with flat structure for new projects:

```
my-project/
├── CLAUDE.md
├── README.md
├── plan.md
├── architecture.md
└── src/
```

### Graduating to Nested

When your project grows (20+ tasks, multiple phases), migrate:

**Step 1:** Create the directory structure
```bash
mkdir -p project/{planning,specs,architecture,sessions}
```

**Step 2:** Move and split existing files
```bash
# Move plan.md content
mv plan.md project/planning/devplan.md
# Create progress tracker
touch project/planning/devprogress.md

# Split architecture if needed
mv architecture.md project/architecture/overview.md

# Create first spec from requirements
mv requirements.md project/specs/00-overview.md
```

**Step 3:** Update CLAUDE.md references
```markdown
## Documentation Structure

This project uses the nested documentation pattern:
- Planning: `project/planning/`
- Specifications: `project/specs/`
- Architecture: `project/architecture/`
- Session notes: `project/sessions/`
```

### Migration Prompt

Ask Claude to help migrate:

```
My project has grown and I need to migrate from flat to nested
documentation structure. Current files:
- plan.md (tasks and progress)
- architecture.md (system design)
- requirements.md (features)

Please:
1. Create project/ directory structure
2. Split plan.md into devplan.md and devprogress.md
3. Move architecture.md to project/architecture/
4. Split requirements into separate spec files per feature
5. Update CLAUDE.md to reference new structure

Preserve all existing content during migration.
```

---

## Feature Documentation Deep Dive

For larger features that span multiple days or involve complex requirements, use this comprehensive documentation approach.

### The Five Document Types

When planning a significant feature, create these five interconnected documents:

| Document | Purpose | Location |
|----------|---------|----------|
| Planning | High-level overview, decisions, timeline | `/docs/planning/features/{feature}.md` |
| Architecture | Technical design, system interactions | `/docs/architecture/{feature}-architecture.md` |
| API Contracts | Endpoint specifications, request/response | `/docs/specs/{feature}/api-contracts.md` |
| User Journey | Personas, flows, edge cases | `/docs/specs/{feature}/user-journey.md` |
| UI Wireframes | Page layouts, component specs | `/docs/specs/{feature}/ui-wireframes.md` |

### Feature Planning Document

**Purpose:** High-level overview, key decisions, timeline, and success criteria.

```markdown
# Feature: {Feature Name}

**Status:** Planning | In Progress | Complete
**Priority:** High | Medium | Low
**Last Updated:** YYYY-MM-DD

## Related Documentation
- [Architecture](../architecture/{feature}-architecture.md)
- [API Contracts](../specs/{feature}/api-contracts.md)
- [UI Wireframes](../specs/{feature}/ui-wireframes.md)
- [User Journey](../specs/{feature}/user-journey.md)

## Overview
{2-3 paragraphs describing the feature, its value, and high-level approach}

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {Decision 1} | {Choice made} | {Why this choice} |

## Scope

### In Scope
- {Item 1}
- {Item 2}

### Out of Scope (Deferred)
- {Item 1} - {Reason}

## Implementation Phases

### Phase 1: {Name}
- [ ] Task 1
- [ ] Task 2

### Phase 2: {Name}
- [ ] Task 1

## Critical Files

**Backend:**
- `path/to/file.go` - {Purpose}

**Frontend:**
- `path/to/component.tsx` - {Purpose}

**Database:**
- `migrations/xxx_create_table.sql`

## Success Criteria

### By End of Phase 1
- [ ] Metric 1 achieved
- [ ] Metric 2 achieved
```

### Feature Architecture Document

**Purpose:** Technical design, database schema, API design, and integration points.

**Key Patterns:**

**ASCII System Diagrams:**
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│   UI    │────▶│   API   │────▶│  Queue  │
└─────────┘     └─────────┘     └────┬────┘
                                     │
                    ┌────────────────┘
                    ▼
              ┌──────────┐     ┌──────────┐
              │ Worker   │────▶│ Database │
              └──────────┘     └──────────┘
```

**Database Schema with Indexes:**
```sql
CREATE TABLE feature_items (
    id SERIAL PRIMARY KEY,
    org_id INT NOT NULL REFERENCES organizations(id),
    user_id INT NOT NULL REFERENCES users(id),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feature_items_org ON feature_items(org_id);
CREATE INDEX idx_feature_items_status ON feature_items(status);
```

**Pipeline Stage Tables:**

| Stage | Duration | Description |
|-------|----------|-------------|
| 1. Validate | <1s | Input validation |
| 2. Process | ~5s | Core transformation |
| 3. Verify | ~10s | Output verification |

### API Contracts Document

**Purpose:** Complete endpoint specifications with request/response examples.

```markdown
### POST /api/v1/items

Create a new item.

**Request:**
```json
{
  "name": "Example",
  "type": "standard",
  "options": {
    "auto_process": true
  }
}
```

**Response (201 Created):**
```json
{
  "id": 123,
  "name": "Example",
  "status": "pending",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400` - Invalid request body
- `401` - Unauthorized
- `409` - Duplicate item
- `422` - Validation failed
```

**Error Code Table:**

| Code | HTTP | Description |
|------|------|-------------|
| VALIDATION_FAILED | 422 | Input validation error |
| DUPLICATE_ITEM | 409 | Item already exists |

### User Journey Document

**Purpose:** User personas, step-by-step flows, edge cases.

**Persona Template:**
```markdown
### Persona: Power User

**Background:** Experienced with similar tools, uses features daily
**Goals:**
- Complete tasks quickly with minimal clicks
- Access advanced options when needed
**Pain Points:**
- Frustrated by unnecessary confirmations
- Needs keyboard shortcuts
```

**Journey Map:**
```markdown
### Journey: Create New Item

**Duration:** 30-60 seconds
**Steps:**

1. **Navigate** → User clicks "New Item" button
   - System displays creation form

2. **Configure** → User fills required fields
   - System validates in real-time

3. **Submit** → User clicks "Create"
   - System shows progress indicator

4. **Complete** → System shows success
   - User redirected to item detail page
```

**Edge Case Pattern:**
```markdown
### Edge Case: Network Interruption During Processing

**Scenario:** User loses connection mid-process
**Expected Behavior:**
1. System retries automatically (3 attempts)
2. If still failing, shows "Processing paused" status
3. User can retry manually when connection restored
**Recovery:** Resume button triggers retry from last checkpoint
```

### UI Wireframes Document

**Purpose:** Page layouts, component specifications, responsive design.

**ASCII Wireframe:**
```
### Item List Page

┌─────────────────────────────────────────────────┐
│  [Logo]    Dashboard  Items  Settings    [User] │
├─────────────────────────────────────────────────┤
│                                                 │
│  Items                          [+ New Item]    │
│  ─────────────────────────────────────────────  │
│                                                 │
│  [Search...          ]  [Filter ▼]  [Sort ▼]   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ ○ Item Name          Status    Created  │   │
│  ├─────────────────────────────────────────┤   │
│  │ ○ Example Item 1     ● Active  Jan 15   │   │
│  │ ○ Example Item 2     ○ Draft   Jan 14   │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Showing 1-10 of 45         [< 1 2 3 4 5 >]    │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Component Specification:**
```markdown
### StatusBadge Component

**Props:**
| Prop | Type | Required | Description |
|------|------|----------|-------------|
| status | string | Yes | 'pending' | 'active' | 'failed' |
| size | string | No | 'sm' | 'md' | 'lg' (default: 'md') |
```

---

## Cross-Referencing Pattern

All feature documents should reference each other for easy navigation:

```markdown
## Related Documentation

| Document | Description |
|----------|-------------|
| [Planning](../planning/features/item-management.md) | Timeline and decisions |
| [Architecture](../architecture/item-architecture.md) | Technical design |
| [API Contracts](./api-contracts.md) | Endpoint specifications |
| [User Journey](./user-journey.md) | User flows |
| [UI Wireframes](./ui-wireframes.md) | Visual layouts |
```

---

## Feature Documentation Checklist

Before implementation begins, verify all documentation is complete:

### Planning Document
- [ ] Key decisions documented with rationale
- [ ] Implementation phases defined
- [ ] Critical files listed
- [ ] Success criteria measurable

### Architecture Document
- [ ] System diagram shows all components
- [ ] Database schema complete with indexes
- [ ] API endpoint summary table
- [ ] Error handling strategy defined

### API Contracts
- [ ] All endpoints documented
- [ ] Request/response examples provided
- [ ] Error codes defined
- [ ] Authentication requirements clear

### User Journey
- [ ] Personas identified
- [ ] Happy path documented
- [ ] Edge cases considered
- [ ] Error UX defined

### UI Wireframes
- [ ] All pages wireframed
- [ ] Component props specified
- [ ] Responsive breakpoints defined
- [ ] Navigation integration shown

---

## Design Review Process

Design reviews validate specifications before implementation, catching issues early when changes are cheap.

### Review Stages

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Draft     │────▶│   Review    │────▶│  Approved   │────▶│ Implement   │
│ (Author)    │     │ (Team)      │     │ (Sign-off)  │     │ (Dev)       │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │
      │ Iterate           │ Request
      └───────────────────┘ Changes
```

### Stage 1: Self-Review (Author)

Before sharing, the author verifies:
- [ ] All five document types are complete
- [ ] Cross-references link correctly
- [ ] No placeholder text remains
- [ ] Examples are realistic and consistent

### Stage 2: Technical Review (Peers)

**Participants:** 2-3 engineers familiar with affected systems

**Focus Areas:**

| Focus | Questions to Answer |
|-------|---------------------|
| Architecture | Does this integrate cleanly? Any conflicts? |
| API Design | Are endpoints RESTful? Consistent patterns? |
| Database | Are indexes sufficient? Migration concerns? |
| Security | Authentication handled? Input validation complete? |
| Performance | Any N+1 queries? Caching strategy needed? |

### Stage 3: Approval and Sign-off

**Requirements:**
- All blocking comments resolved
- At least 2 technical approvals
- Stakeholder approval (if applicable)

**Sign-off Format:**
```markdown
## Approvals

| Role | Name | Date | Status |
|------|------|------|--------|
| Tech Lead | {Name} | YYYY-MM-DD | Approved |
| Senior Dev | {Name} | YYYY-MM-DD | Approved |
```

---

## Spec Versioning and Change Management

### Version Header

Every spec document should include:

```markdown
# Feature: Item Management

**Version:** 1.2.0
**Status:** Approved
**Last Updated:** 2025-01-15
**Author:** {Name}

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.2.0 | 2025-01-15 | {Name} | Added batch processing endpoint |
| 1.1.0 | 2025-01-10 | {Name} | Updated validation rules |
| 1.0.0 | 2025-01-05 | {Name} | Initial approved version |
```

### Semantic Versioning for Specs

| Version Bump | When to Use | Example |
|--------------|-------------|---------|
| **Major (X.0.0)** | Breaking changes | Removing endpoint, changing auth model |
| **Minor (1.X.0)** | Additive changes | New endpoint, new optional field |
| **Patch (1.0.X)** | Clarifications | Better examples, formatting fixes |

### Change Request Process

When specs need to change during implementation:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Change    │────▶│   Impact    │────▶│   Review    │
│  Identified │     │  Analysis   │     │  & Approve  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                    ┌─────────────────────────┘
                    ▼
              ┌─────────────┐     ┌─────────────┐
              │   Update    │────▶│  Notify     │
              │   Specs     │     │  Team       │
              └─────────────┘     └─────────────┘
```

### Document Lifecycle States

| Status | Meaning | Can Edit? |
|--------|---------|-----------|
| **Draft** | Initial writing | Yes, freely |
| **In Review** | Under team review | Yes, based on feedback |
| **Approved** | Ready for implementation | Only via change request |
| **In Progress** | Implementation underway | Only via change request |
| **Implemented** | Feature shipped | Archive only |
| **Deprecated** | Replaced by newer spec | No changes |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Writing docs after implementation | Docs become stale/incomplete | Document during planning phase |
| Single monolithic spec | Hard to navigate and update | Split into focused documents |
| No cross-references | Readers can't find related info | Add Related Documentation section |
| Missing error scenarios | Edge cases discovered in production | Document error handling explicitly |
| Vague success criteria | No way to verify completion | Use measurable, specific goals |
| No file list | Code reviews miss scope | List all files to create/modify |

---

## Quick Reference Card

### Flat Structure Checklist
- [ ] CLAUDE.md - Project configuration
- [ ] README.md - Quick start and overview
- [ ] plan.md - Tasks and progress
- [ ] architecture.md - System design
- [ ] requirements.md - Feature requirements
- [ ] ui-specs.md - UI specifications (if applicable)

### Nested Structure Checklist
- [ ] CLAUDE.md - Project configuration
- [ ] README.md - Quick start and overview
- [ ] project/planning/devplan.md - Master plan
- [ ] project/planning/devprogress.md - Progress tracker
- [ ] project/planning/database.md - Schema documentation
- [ ] project/specs/*.md - Feature specifications
- [ ] project/architecture/*.md - Architecture documents
- [ ] project/sessions/*.md - Session summaries

### File Update Frequency

| File | Update Frequency |
|------|------------------|
| CLAUDE.md | When conventions change |
| README.md | When setup changes |
| plan.md / devplan.md | Start of each phase |
| devprogress.md | After each task |
| architecture.md | When design changes |
| specs/*.md | Before implementing feature |
| sessions/*.md | End of each session |

---

**Prev:** [Git Workflow](./11-git-workflow.md) | **Next:** [Documentation Writing](./13-documentation-writing.md)

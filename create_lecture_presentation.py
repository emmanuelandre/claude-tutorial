#!/usr/bin/env python3
"""
Generate 1-hour AI-First Development lecture presentation.
No hands-on exercises - practitioner-level depth with actionable takeaways.
Tool-agnostic with Claude Code/Windsurf as examples.
"""

from reportlab.lib.styles import getSampleStyleSheet
from presentation_utils import (
    create_document,
    create_title_slide,
    create_section_slide,
    create_content_slide,
    create_two_column_slide,
    create_code_slide,
    create_thank_you_slide,
    NumberedCanvas
)


def create_presentation():
    """Generate the complete lecture presentation."""
    doc = create_document("ai-first-lecture.pdf")
    styles = getSampleStyleSheet()
    story = []

    # =================
    # TITLE
    # =================
    create_title_slide(
        story, styles,
        "AI-First Development",
        "A Practitioner's Guide",
        "Applicable to Claude Code, Windsurf, Cursor, and other AI coding assistants"
    )

    # =================
    # AGENDA
    # =================
    create_content_slide(story, styles, "Agenda", [
        "1. AI-First Philosophy",
        "2. Addressing Common Concerns",
        "3. Prompt Engineering vs Vibe Coding",
        "4. Getting Started with Prompt Engineering",
        "5. Scaling to Large Projects",
        "6. Best Practices for Feature Documentation",
        "7. Testing Strategies",
        "8. Project Planning & Workflow",
        "9. Git Best Practices",
        "10. Tips & Tricks"
    ])

    # =================
    # SECTION 1: AI-FIRST PHILOSOPHY
    # =================
    create_section_slide(story, styles, "1. AI-First Philosophy")

    create_content_slide(story, styles, "What is AI-First Development?", [
        "Traditional: Human writes code → AI assists occasionally",
        "AI-First: AI executes 100% → Human validates 100%",
        ("Key distinction:", [
            "AI handles ALL coding, testing, documentation",
            "Human handles ALL validation, review, decisions",
            "Clear handoff points at each step"
        ]),
        "Takeaway: Humans become architects & validators, AI becomes the builder"
    ])

    create_content_slide(story, styles, "Core Development Principles", [
        ("Specifications Drive Implementation:", [
            "Database schema → API contracts → UI components",
            "Write specs BEFORE AI implements"
        ]),
        ("Micro-Teams of 2:", [
            "2 humans + AI assistant = redundancy without overhead",
            "Each team owns end-to-end features"
        ]),
        ("Own Your Stack:", [
            "Be your own QA engineer",
            "Be your own DevOps engineer",
            "Own the entire vertical slice"
        ])
    ])

    create_content_slide(story, styles, "The Paradigm Shift", [
        ("From:", [
            '"AI helps me write code"',
            '"Let me ask AI to fix this bug"',
            '"AI suggests completions"'
        ]),
        ("To:", [
            '"AI executes my specifications"',
            '"I validate what AI produced"',
            '"AI implements the full feature"'
        ]),
        "Takeaway: Treat AI as your execution engine, not just an assistant"
    ])

    create_content_slide(story, styles, "When AI-First Works Best", [
        ("Ideal scenarios:", [
            "New features with clear requirements",
            "CRUD operations and API endpoints",
            "Test generation and documentation",
            "Refactoring with defined patterns"
        ]),
        ("Less ideal scenarios:", [
            "Real-time pair programming",
            "Highly visual design work",
            "Hardware-specific debugging"
        ])
    ])

    # =================
    # SECTION 2: ADDRESSING COMMON CONCERNS
    # =================
    create_section_slide(story, styles, "2. Addressing Common Concerns")

    create_content_slide(story, styles, "Common Concerns Engineers Raise", [
        "1. Code Quality & Reliability - Hallucinations, hidden bugs",
        "2. Security Risks - Insecure patterns, data exposure",
        "3. Maintainability - Opaque code, inconsistent style",
        "4. Design Integrity - Architecture drift, loss of intent",
        "5. Testing & Validation - False sense of coverage",
        "6. IP & Compliance - License ambiguity",
        "7. Developer Experience - Skill atrophy",
        "8. Accountability - Who owns AI-generated bugs?"
    ])

    create_content_slide(story, styles, "Code Quality & Security", [
        ("The Concern:", [
            "AI generates syntactically correct but logically flawed code",
            "AI might introduce vulnerabilities"
        ]),
        ("How We Address It:", [
            "Human validates 100% - every line is reviewed",
            "Mandatory E2E tests catch integration issues",
            "Pre-commit checks enforce quality gates",
            "Three-layer review: Self → Automated → Peer"
        ]),
        "Takeaway: Trust but verify - always review AI output"
    ])

    create_content_slide(story, styles, "Maintainability & Design", [
        ("The Concern:", [
            "AI-generated code hard to understand",
            "May not follow team conventions",
            "Optimizes locally, not holistically"
        ]),
        ("How We Address It:", [
            "Project rules file defines conventions (CLAUDE.md, .windsurfrules)",
            "Architecture documented upfront",
            "Human writes specs BEFORE AI implements",
            "AI follows existing patterns"
        ]),
        "Takeaway: Document your standards where AI can read them"
    ])

    create_content_slide(story, styles, "Testing, IP & Accountability", [
        ("Testing:", [
            "Test-first approach - define tests before implementation",
            "Human verifies test quality, not just coverage"
        ]),
        ("IP & Compliance:", [
            "Review AI suggestions for license issues",
            "Keep audit trail in commit history"
        ]),
        ("Accountability:", [
            "Human approves every PR = human owns the code",
            "Git history shows human review at each step"
        ]),
        "Takeaway: Human approval = Human ownership"
    ])

    create_content_slide(story, styles, "The Bottom Line", [
        "AI-First ≠ AI-Only",
        ("The methodology addresses concerns through:", [
            "Systematic validation at every step",
            "Comprehensive testing (E2E + Unit)",
            "Clear human ownership and accountability",
            "Documented conventions in project rules"
        ]),
        "Result: Faster development WITH maintained quality"
    ])

    # =================
    # SECTION 3: PROMPT VS VIBE
    # =================
    create_section_slide(story, styles, "3. Prompt Engineering vs Vibe Coding")

    create_content_slide(story, styles, "What is Vibe Coding?", [
        "Informal, exploratory approach with minimal instructions",
        ("Characteristics:", [
            "Speed over precision",
            'AI "guesses" intent',
            "Minimal context provided"
        ]),
        'Example: "Make something that sorts numbers"',
        ("Result:", [
            "Quick for prototypes",
            "Unpredictable code quality"
        ])
    ])

    create_content_slide(story, styles, "What is Prompt Engineering?", [
        "Precise, structured inputs to guide AI behavior",
        ("Characteristics:", [
            "Context and constraints provided",
            "Clear success criteria",
            "Examples included when helpful"
        ]),
        'Example: "Write Python function to sort integers ascending, no built-in sort, return new list"',
        "Result: Predictable, production-ready code"
    ])

    create_two_column_slide(
        story, styles,
        "Side-by-Side Comparison",
        "Vibe Coding",
        [
            "Fast initial results",
            "Unpredictable quality",
            "Best for prototypes",
            "More rework later",
            "Hard to maintain"
        ],
        "Prompt Engineering",
        [
            "Slower initial setup",
            "Consistent quality",
            "Best for production",
            "Less rework overall",
            "Easy to maintain"
        ]
    )

    create_content_slide(story, styles, "When to Use Each", [
        ("Use Vibe Coding for:", [
            "Quick prototypes and experiments",
            "Exploring APIs or libraries",
            "Throwaway code"
        ]),
        ("Use Prompt Engineering for:", [
            "Production code",
            "Team projects",
            "Anything that will be maintained",
            "Code that needs tests"
        ]),
        "Takeaway: Default to prompt engineering for professional work"
    ])

    # =================
    # SECTION 4: PROMPT ENGINEERING
    # =================
    create_section_slide(story, styles, "4. Getting Started with Prompt Engineering")

    create_content_slide(story, styles, "Core Prompt Principles", [
        ("Be Specific:", [
            'Not "fix the bug" but "fix the race condition in token refresh"'
        ]),
        ("Provide Context:", [
            "Architecture, patterns, constraints",
            "Reference specific files"
        ]),
        ("Define Success:", [
            "What should work when done?",
            "What tests should pass?"
        ]),
        "Takeaway: Treat prompts like specifications"
    ])

    create_two_column_slide(
        story, styles,
        "Good vs Bad Prompts",
        "❌ Bad Prompts",
        [
            '"Add search to the API"',
            '"Fix the authentication"',
            '"Make it faster"',
            '"Add validation"'
        ],
        "✅ Good Prompts",
        [
            '"Add search: filter by email/name, case-insensitive, debounce 300ms"',
            '"Fix token refresh race condition when concurrent API calls"',
            '"Add pagination to /users endpoint, 20 per page, cursor-based"',
            '"Validate email format and password min 8 chars on registration"'
        ]
    )

    create_content_slide(story, styles, "Prompt Patterns", [
        ("Feature Request:", [
            "Requirements → Technical Details → Success Criteria"
        ]),
        ("Bug Fix:", [
            "Expected vs Actual → Steps to Reproduce → Error Message"
        ]),
        ("Multi-Step:", [
            "Break into numbered steps",
            "Define validation at each step"
        ]),
        "Takeaway: Use templates for consistent results"
    ])

    create_code_slide(story, styles, "Example: Well-Structured Prompt", "prompt",
"""I need to implement user authentication for my API.

Requirements:
- Users register with email/password
- JWT tokens for authentication
- Password hashing with bcrypt

API Endpoints:
POST /api/auth/register - Register new user
POST /api/auth/login - Login and get JWT

Success Criteria:
- Passwords never stored in plain text
- JWT expires after 1 hour
- E2E tests cover happy path and error cases

Please create the database migration first.""")

    create_content_slide(story, styles, "Common Prompt Mistakes", [
        ("Over-reliance:", [
            '"Build me a complete e-commerce platform"',
            "Fix: Break into smaller, specific requests"
        ]),
        ("Under-specification:", [
            '"Add validation"',
            "Fix: Specify what to validate and how"
        ]),
        ("Forgetting Tests:", [
            '"Implement user authentication"',
            'Fix: Add "Include E2E tests for..."'
        ])
    ])

    # =================
    # SECTION 5: SCALING LARGE PROJECTS
    # =================
    create_section_slide(story, styles, "5. Scaling to Large Projects")

    create_content_slide(story, styles, "The Challenge of Large Projects", [
        ("When projects grow:", [
            "100+ tasks across modules",
            "Complex dependencies",
            "Context loss between sessions"
        ]),
        ("The Solution:", [
            "Phased development",
            "Centralized planning structure",
            "Continuous progress tracking"
        ])
    ])

    create_content_slide(story, styles, "Project Planning Structure", [
        ("Directory Layout:", [
            "project/planning/ - Master plan and progress",
            "project/specs/ - Feature specifications",
            "project/sessions/ - Session summaries"
        ]),
        ("Key Files:", [
            "devplan.md - Master plan with phases and dependencies",
            "devprogress.md - Progress tracker with checkboxes",
            "database.md - Schema documentation"
        ]),
        "Takeaway: Organize documentation for AI consumption"
    ])

    create_content_slide(story, styles, "The Master Plan (devplan.md)", [
        ("Contains:", [
            "Phases with clear objectives",
            "Dependency mapping between features",
            "Tasks with checkboxes"
        ]),
        ("Workflow per Feature:", [
            "DB → API → Tests → UI → UI Tests",
            "Complete each layer before moving on",
            "Never skip testing"
        ])
    ])

    create_content_slide(story, styles, "Progress Tracking (devprogress.md)", [
        ("Update After Every Session:", [
            "Mark completed tasks [x]",
            "Update phase percentages",
            "Document blockers"
        ]),
        ("Quick Stats Table:", [
            "Phase | Status | Progress",
            "🔴 Not Started | 🟡 In Progress | 🟢 Complete"
        ]),
        "Takeaway: Update progress religiously - it's your context for next session"
    ])

    create_content_slide(story, styles, "When to Use What", [
        ("Small Projects (<20 tasks):", [
            "Simple project rules file is enough"
        ]),
        ("Medium Projects (20-50 tasks):", [
            "Add devplan.md and devprogress.md"
        ]),
        ("Large Projects (50+ tasks):", [
            "Full planning structure",
            "Session notes after every session"
        ]),
        "Takeaway: Scale documentation with project complexity"
    ])

    # =================
    # SECTION 6: FEATURE DOCUMENTATION
    # =================
    create_section_slide(story, styles, "6. Best Practices for Feature Documentation")

    create_content_slide(story, styles, "The 5-Document Approach", [
        "For large features, create 5 documents:",
        ("1. Planning Document (What & When):", [
            "Timeline, scope, decisions, success criteria"
        ]),
        ("2. Architecture Document (How):", [
            "System diagrams, database schema, error handling"
        ]),
        ("3. API Contracts (Interface):", [
            "Endpoints, request/response examples, error codes"
        ]),
        ("4. User Journey (Experience):", [
            "Personas, step-by-step flows, edge cases"
        ]),
        ("5. UI Wireframes (Visuals):", [
            "Page layouts, component specs, responsive design"
        ])
    ])

    create_content_slide(story, styles, "Planning Document Structure", [
        ("Key Sections:", [
            "Related Documentation - links to other docs",
            "Overview - problem statement and solution",
            "Key Decisions - with rationale",
            "Scope - what's in and explicitly out",
            "Implementation Phases - with tasks",
            "Critical Files - all files to create/modify",
            "Success Criteria - measurable goals"
        ]),
        "Takeaway: Explicit scope prevents scope creep"
    ])

    create_content_slide(story, styles, "Architecture & API Contracts", [
        ("Architecture Document:", [
            "ASCII system diagrams showing component interactions",
            "Complete database schema with indexes",
            "Error handling strategies"
        ]),
        ("API Contracts:", [
            "Endpoint summary table",
            "Request/response JSON examples",
            "Error codes with descriptions"
        ]),
        "Takeaway: AI produces better code with precise contracts"
    ])

    create_content_slide(story, styles, "Design Review Process", [
        ("Review Stages:", [
            "Draft → Review → Approved → Implement"
        ]),
        ("Technical Review Focus:", [
            "Architecture - does it integrate cleanly?",
            "API Design - RESTful and consistent?",
            "Database - indexes sufficient?",
            "Security - auth and validation complete?"
        ]),
        "Takeaway: Catch issues early when changes are cheap"
    ])

    # =================
    # SECTION 7: TESTING STRATEGIES
    # =================
    create_section_slide(story, styles, "7. Testing Strategies")

    create_content_slide(story, styles, "Modern Testing Philosophy", [
        "Both E2E and Unit tests are MANDATORY",
        ("E2E Tests (Required):", [
            "Complete user journeys",
            "API endpoint testing",
            "UI workflow testing"
        ]),
        ("Unit Tests (Required):", [
            "Business logic",
            "Utilities and helpers",
            "Edge cases and data transformations"
        ]),
        ("Component Tests (When applicable):", [
            "Microservices integration",
            "Database operations with test containers"
        ])
    ])

    create_content_slide(story, styles, "Test-First Approach", [
        ("Before Implementation:", [
            "Define coverage targets (70-90%)",
            "Build testing infrastructure first",
            "Document test scenarios"
        ]),
        ("During Implementation:", [
            "Write tests alongside code",
            "Run tests frequently",
            "Don't proceed if tests fail"
        ]),
        "Takeaway: Tests are your regression safety net"
    ])

    create_content_slide(story, styles, "Testing Best Practices", [
        "Test user journeys, not implementation details",
        "Use data-test attributes for stable selectors",
        ("Coverage priorities:", [
            "Happy path - must pass",
            "Critical failures - invalid inputs, permissions",
            "Edge cases - boundary conditions",
            "Error scenarios - network failures, timeouts"
        ]),
        "Run tests in pre-commit hooks",
        "Takeaway: Tests that run automatically get run consistently"
    ])

    create_content_slide(story, styles, "Coverage Measurement", [
        ("Track coverage from all test types:", [
            "Unit test coverage",
            "E2E test coverage",
            "Component test coverage (if applicable)"
        ]),
        ("Merge coverage reports:", [
            "See the complete picture",
            "Identify gaps"
        ]),
        "Takeaway: Measure coverage from ALL test types combined"
    ])

    # =================
    # SECTION 8: PROJECT PLANNING
    # =================
    create_section_slide(story, styles, "8. Project Planning & Workflow")

    create_content_slide(story, styles, "The 10-Step Development Process", [
        "1. Specification (Human writes detailed spec)",
        "2. Database Schema (AI designs → Human reviews)",
        "3. Repository Layer (AI implements → Human reviews)",
        "4. API Endpoints (AI creates → Human reviews)",
        "5. API E2E Tests (AI writes → Human verifies)",
        "6. Frontend Components (AI builds → Human reviews)",
        "7. UI E2E Tests (AI creates → Human verifies)",
        "8. Documentation (AI updates → Human reviews)",
        "9. Code Review (Human conducts)",
        "10. Deployment (AI executes → Human verifies)"
    ])

    create_content_slide(story, styles, "Handoffs & Quality Gates", [
        ("Each Step Has:", [
            "Clear deliverables",
            "Human approval checkpoint",
            "Tests that must pass"
        ]),
        ("Quality Gates:", [
            "Schema reviewed before repository",
            "API tests pass before frontend",
            "All tests pass before PR"
        ]),
        "Takeaway: Never skip a step, never skip a review"
    ])

    create_two_column_slide(
        story, styles,
        "AI vs Human Responsibilities",
        "AI Executes",
        [
            "Design database schema",
            "Implement repository layer",
            "Create API endpoints",
            "Write tests",
            "Build UI components",
            "Update documentation",
            "Execute deployment"
        ],
        "Human Validates",
        [
            "Write specifications",
            "Review all code",
            "Verify tests are meaningful",
            "Conduct code review",
            "Merge pull requests",
            "Make architectural decisions"
        ]
    )

    # =================
    # SECTION 9: GIT BEST PRACTICES
    # =================
    create_section_slide(story, styles, "9. Git Best Practices")

    create_content_slide(story, styles, "Branch Naming & Commits", [
        ("Branch Naming: <type>/<description>", [
            "feature/user-auth",
            "fix/login-bug",
            "refactor/api-cleanup",
            "docs/readme-update"
        ]),
        ("Conventional Commits: <type>(<scope>): <subject>", [
            "feat(auth): add Google OAuth login",
            "fix(api): handle null user gracefully",
            "test(auth): add E2E tests for login flow"
        ]),
        "Takeaway: Consistent naming enables automation"
    ])

    create_content_slide(story, styles, "Pre-Commit Checks (Mandatory)", [
        ("Must Run Before Every Commit:", [
            "Lint - code formatting and style",
            "Tests - unit and E2E tests",
            "Build - verify it compiles/bundles"
        ]),
        ("Set Up Hooks:", [
            "Use husky (Node) or pre-commit (Python)",
            "Fail commit if any check fails"
        ]),
        "Takeaway: Catch issues locally, not in PR review"
    ])

    create_content_slide(story, styles, "Hard Rules", [
        "❌ Never commit directly to main",
        "❌ Never merge your own PR without review",
        "❌ Never commit code that fails tests",
        "❌ Never commit secrets (.env, credentials)",
        "❌ Never force push to main",
        ("AI Boundaries:", [
            "✅ AI can: create branches, commit, push, open PRs",
            "❌ AI cannot: merge PRs, approve PRs"
        ]),
        "Takeaway: Humans control what gets merged"
    ])

    # =================
    # SECTION 10: TIPS & TRICKS
    # =================
    create_section_slide(story, styles, "10. Tips & Tricks")

    create_content_slide(story, styles, "Communication Tips", [
        ("Be Specific:", [
            '"Fix the race condition in token refresh" not "fix the bug"'
        ]),
        ("Reference Files:", [
            '"In src/models/user.ts, add email_verified field"'
        ]),
        ("Request Explanations:", [
            '"Implement and explain the trade-offs"'
        ]),
        ("Verify Understanding:", [
            '"Before implementing, confirm: Goal is X, constraints are Y"'
        ])
    ])

    create_content_slide(story, styles, "Productivity Techniques", [
        ("Multi-Step Requests:", [
            "Number your steps",
            "Define validation at each step"
        ]),
        ("Batch Related Changes:", [
            '"Update all error responses to use format X"'
        ]),
        ("Progressive Refinement:", [
            "Basic → Add feature → Add polish"
        ]),
        ("Start Sessions with Context:", [
            '"Continuing work on X. Last session we did Y."'
        ])
    ])

    create_content_slide(story, styles, "Working with Large Codebases", [
        ("Navigate:", [
            '"Show me all files that handle authentication"'
        ]),
        ("Understand First:", [
            '"Explain how the current auth flow works"'
        ]),
        ("Refactor Safely:", [
            '"Refactor X to Y. Ensure all existing tests pass."'
        ]),
        "Takeaway: Use AI to explore unfamiliar code"
    ])

    create_content_slide(story, styles, "Pro Tips Summary", [
        "Start sessions with context",
        "End sessions with notes (what was done, what's next)",
        "Use checkpoints - commit after each logical step",
        "Trust but verify - always review AI output",
        "Keep project rules file current",
        "Build a prompt library for your team",
        "Takeaway: Document what prompts work for your project"
    ])

    # =================
    # SUMMARY
    # =================
    create_section_slide(story, styles, "Summary & Action Plan")

    create_content_slide(story, styles, "Key Takeaways", [
        "✓ AI-First: AI executes 100%, Human validates 100%",
        "✓ Prompt Engineering > Vibe Coding for production",
        "✓ Project rules file is essential",
        "✓ 10-step workflow with clear handoffs",
        "✓ E2E + Unit tests are both mandatory",
        "✓ Pre-commit checks are non-negotiable",
        "✓ Humans control what gets merged"
    ])

    create_content_slide(story, styles, "Your Action Plan", [
        ("Start Today:", [
            "Create a project rules file for your current project"
        ]),
        ("Next Feature:", [
            "Use the 10-step process",
            "Write specs BEFORE AI implements"
        ]),
        ("As Projects Grow:", [
            "Add planning structure (devplan.md, devprogress.md)"
        ]),
        ("Resources:", [
            "Claude Code: claude.ai/code",
            "Windsurf: codeium.com/windsurf",
            "Cursor: cursor.sh"
        ])
    ])

    # =================
    # THANK YOU
    # =================
    create_thank_you_slide(story, styles, "Thank You!", "Questions?")

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print("✅ Lecture presentation created: ai-first-lecture.pdf")


if __name__ == "__main__":
    create_presentation()

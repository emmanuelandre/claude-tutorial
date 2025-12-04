# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a comprehensive tutorial and best practices guide for working with Claude Code. It contains documentation, workshop materials, and templates teaching developers how to use Claude Code effectively for AI-first software development.

## Repository Purpose

This repository provides:
- Educational documentation about Claude Code workflows
- Workshop materials including interactive presentations
- Templates and examples (especially CLAUDE.md templates)
- Best practices for AI-first development methodology

## Architecture

This is a **documentation-only repository** with the following structure:

```
claude-tutorial/
├── docs/                           # Main tutorial content
│   ├── 01-introduction.md          # What is Claude Code
│   ├── 02-quick-start.md           # 5-minute getting started
│   ├── 03-setup-guide.md           # Comprehensive setup
│   ├── 04-claude-md.md             # CLAUDE.md file guide
│   ├── 05-prompt-engineering.md    # Writing effective prompts
│   ├── 06-testing-strategy.md      # E2E-first testing philosophy
│   ├── 07-ai-first-workflow.md     # 10-step development process
│   ├── 08-feature-workflow.md      # End-to-end feature development
│   ├── 09-project-planning-structure.md  # Project organization
│   ├── 11-git-workflow.md          # Git conventions and workflow
│   ├── 19-troubleshooting.md       # Common issues and solutions
│   ├── 20-tips-tricks.md           # Power user techniques
│   └── 21-resources.md             # Additional resources
│
├── examples/
│   └── claude-md-template.md       # Production-ready CLAUDE.md template
│
├── prompts.md                      # Original workshop exercise prompts
├── workshop-prompts.md             # Hands-on workshop prompts (auto-generated)
├── WORKSHOP_GUIDE.md               # Instructor guide for workshops
│
├── # Presentation PDFs
├── claude-code-interactive-tutorial.pdf   # Original interactive workshop (2-3 hours)
├── ai-first-lecture.pdf            # 1-hour lecture (no hands-on)
├── ai-first-workshop.pdf           # 3-hour hands-on workshop
│
├── # Python scripts to generate presentations
├── presentation_utils.py           # Shared utilities for PDF generation
├── create_presentation.py          # Generates overview PDF
├── create_interactive_presentation_v2.py  # Generates interactive tutorial PDF
├── create_lecture_presentation.py  # Generates 1-hour lecture PDF
└── create_handson_workshop.py      # Generates 3-hour workshop PDF + prompts
```

## Key Concepts (Important for Editing)

When working with this repository, understand these core concepts that are taught:

### 1. The CLAUDE.md Philosophy
- Every software project should have a CLAUDE.md file at its root
- Acts as persistent context across Claude Code sessions
- Contains architecture, conventions, and workflows
- The `examples/claude-md-template.md` is the reference implementation

### 2. Team Structure Terminology
Throughout this tutorial, when we refer to "team of 2" or "micro-teams of 2", we mean:
- **2 human developers + Claude Code** working together
- This provides redundancy without coordination overhead
- Each team owns end-to-end features
- Enables parallel development without bottlenecks

### 3. AI-First Development Workflow
The 10-step systematic process (from `docs/07-ai-first-workflow.md`):
1. Human writes specification
2. AI designs database schema
3. AI implements repository layer
4. AI builds API endpoints
5. AI writes API E2E tests
6. AI implements frontend
7. AI writes UI E2E tests
8. AI updates documentation
9. Human conducts code review
10. AI executes deployment

**Core principle: "AI executes 100%, Humans validate 100%"**

### 4. Testing Philosophy
Test-first approach with comprehensive coverage:
- **E2E tests are mandatory** (comprehensive coverage of user journeys)
- **Unit tests are mandatory** (test business logic, utilities, and edge cases)
- **Component tests are good to have** (use test containers where applicable, e.g., for microservices)
- **Coverage measurement is important** (track coverage from unit, component, and E2E tests)
- Coverage thresholds vary by project, but higher is better
- **Test-first workflow**: Define coverage targets and build testing infrastructure/framework before implementation
- Both E2E and unit tests should run in pre-commit hooks to catch issues early

### 5. Git Workflow Standards
From `docs/11-git-workflow.md`:
- Branch naming: `<type>/<description>` (e.g., `feature/user-auth`, `fix/login-bug`)
- Conventional commits: `<type>(<scope>): <subject>`
- Never commit directly to main
- Humans merge PRs, not AI
- **Pre-commit hooks mandatory**: Run lint, unit tests, and build before every commit
- This catches issues locally before PR review, saving time and iteration cycles

## Working with This Repository

### Documentation Standards

**When editing documentation:**
- Use clear, concise language
- Include practical examples
- Maintain consistent formatting across all docs
- Cross-reference related documents using relative links
- Keep table of contents in README.md updated

**Markdown conventions:**
- Use `##` for main sections, `###` for subsections
- Code blocks must specify language (```javascript, ```bash, ```go, etc.)
- Use ✅ and ❌ for do/don't comparisons
- Include "Prev" and "Next" navigation links at bottom of guides

### Template Maintenance

The `examples/claude-md-template.md` is the **most important file** in this repository:
- It's the reference implementation shown to users
- Must be production-ready and comprehensive
- Should demonstrate all CLAUDE.md best practices
- Updates here should reflect current best practices

### Workshop Materials

The workshop materials work together as a system. There are three presentation options:

**1. Original Interactive Workshop (2-3 hours)**
- `claude-code-interactive-tutorial.pdf` - Interactive tutorial with hands-on exercises
- `prompts.md` - Copy-paste prompts (references slide numbers)
- Best for: Standard workshop sessions

**2. Lecture Presentation (1 hour, no hands-on)**
- `ai-first-lecture.pdf` - Comprehensive lecture covering all topics
- No accompanying prompts file (lecture format)
- Best for: Conference talks, team briefings, executive overviews
- Topics: Philosophy, concerns, prompt engineering, testing, git, tips

**3. Hands-On Workshop (3 hours)**
- `ai-first-workshop.pdf` - Focused on building from scratch
- `workshop-prompts.md` - Copy-paste prompts (auto-generated)
- Reference repo: `github.com/emmanuelandre/unveiling-claude`
- Best for: Full training sessions, bootcamps
- Attendees build their own project using reference examples

**Instructor Guide:**
- `WORKSHOP_GUIDE.md` - Notes for running any workshop format

**Workshop GitHub Repository Convention:**
- All attendees create a private GitHub repository named: `unveiling-claude`
  - Repository URL: `https://github.com/[their-username]/unveiling-claude`
  - Example: `https://github.com/johnsmith/unveiling-claude`
- Repository should be **private** (for learning/practice purposes)
- Used throughout the workshop for exercises and PRs
- Allows attendees to practice real-world Git workflow

**When updating workshop materials:**
- Keep prompts.md in sync with PDF slide numbers
- Ensure exercises are self-contained and work independently
- Test prompts to verify they produce expected results
- Include coverage measurement in all testing exercises

### Python Presentation Scripts

The `create_*.py` files generate presentation PDFs:

| Script | Output | Purpose |
|--------|--------|---------|
| `presentation_utils.py` | (shared module) | Common utilities for all presentations |
| `create_presentation.py` | `claude-code-tutorial.pdf` | Simple 17-slide overview |
| `create_interactive_presentation_v2.py` | `claude-code-interactive-tutorial.pdf` | Original interactive workshop |
| `create_lecture_presentation.py` | `ai-first-lecture.pdf` | 1-hour lecture (no hands-on) |
| `create_handson_workshop.py` | `ai-first-workshop.pdf` + `workshop-prompts.md` | 3-hour hands-on workshop |

**To regenerate presentations:**
```bash
.venv/bin/python3 create_lecture_presentation.py    # Lecture
.venv/bin/python3 create_handson_workshop.py        # Workshop
```

**Dependencies:** `reportlab` (installed in `.venv`)

## Common Tasks

### Adding New Documentation

1. Create new markdown file in `docs/` with number prefix (e.g., `10-new-topic.md`)
2. Add entry to README.md table of contents
3. Add navigation links (Prev/Next) to new doc and adjacent docs
4. Follow existing documentation structure and style

### Updating the CLAUDE.md Template

1. Edit `examples/claude-md-template.md`
2. Ensure changes reflect current best practices
3. Verify template remains comprehensive but not overwhelming
4. Update `docs/04-claude-md.md` if template structure changes significantly

### Fixing Documentation Issues

1. Check cross-references are not broken
2. Verify code examples are syntactically correct
3. Ensure consistency in terminology across all docs
4. Test any commands or code snippets mentioned

### Updating Git Workflow Documentation

When updating `docs/11-git-workflow.md`:
- This is referenced by the CLAUDE.md template
- Changes here affect how users set up their projects
- Keep examples practical and copy-paste ready

## Style Guidelines

### Writing Style
- **Audience**: Developers familiar with software development but new to AI-first workflows
- **Tone**: Practical, direct, experience-based
- **Structure**: Start with concept, show examples, explain why
- **Emphasis**: Use bold for key concepts, not for emphasis

### Code Examples
- Must be complete and runnable (not pseudocode)
- Include comments only when necessary for clarity
- Show both wrong (❌) and right (✅) approaches when helpful
- Use realistic variable names and scenarios

### Formatting Conventions
- **Bold** for core concepts and important terms
- `Code formatting` for commands, file names, code elements
- > Blockquotes for important notes
- Lists for steps or related items
- Tables only when comparing multiple dimensions

## Version Control

### Branch Strategy
Follow the git workflow documented in this repository:
- Use `docs/` prefix for documentation updates
- Use `feat/` prefix for new content
- Use `fix/` prefix for corrections

### Commit Messages
```
docs: add section on MCP servers to quick start
feat: add advanced testing strategies guide
fix: correct code example in git workflow
```

## Key Files Reference

| File | Purpose | Notes |
|------|---------|-------|
| `README.md` | Repository overview and navigation | Main entry point for users |
| `examples/claude-md-template.md` | CLAUDE.md reference implementation | Most important template |
| `docs/04-claude-md.md` | Guide to creating CLAUDE.md files | Explains the template |
| `docs/06-testing-strategy.md` | E2E-first testing philosophy | Core methodology |
| `docs/07-ai-first-workflow.md` | 10-step development process | Core methodology |
| `docs/11-git-workflow.md` | Git conventions and best practices | Referenced by template |
| `prompts.md` | Original workshop exercise prompts | Used with interactive tutorial PDF |
| `workshop-prompts.md` | Hands-on workshop prompts | Auto-generated, used with 3-hour workshop |
| `ai-first-lecture.pdf` | 1-hour lecture slides | No hands-on, conference/briefing format |
| `ai-first-workshop.pdf` | 3-hour workshop slides | Hands-on, build from scratch format |

## Important Notes

**This is NOT a software project**, so:
- No build commands or test suites
- No dependencies to install
- No deployment process
- No runtime environment

**This IS a documentation project**, so:
- Focus on clarity and accuracy of content
- Maintain consistency across all documents
- Keep examples up-to-date with Claude Code features
- Ensure workshop materials work for students

## Philosophy to Maintain

When making changes, preserve these core principles taught in this tutorial:

1. **CLAUDE.md is essential** - Every project needs one
2. **Comprehensive testing** - Both E2E tests (user journeys) and unit tests (business logic) are important
3. **AI executes, Humans validate** - Clear separation of responsibilities
4. **Pre-commit hooks catch issues early** - Lint and tests run locally before pushing to save PR review time
5. **Git workflow discipline** - Never commit to main, all checks must pass before commit
6. **Context is king** - Be explicit and specific in prompts
7. **Iterate and refine** - Progressive improvement over big-bang implementations

---

**Last Updated**: 2025-12-04
**Repository Type**: Educational Documentation
**Primary Audience**: Software developers learning AI-first development with Claude Code
- always update /docs, the pdf slides and the prompts.md
- use python3 not python
- always update workshop pdf, docs and prompts and examples.
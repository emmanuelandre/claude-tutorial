# Workshop Presentation Guide

## Available Presentations

| Presentation | Duration | Format | Use Case |
|--------------|----------|--------|----------|
| `ai-first-lecture.pdf` | 1 hour | Lecture (no hands-on) | Conference talks, team briefings |
| `ai-first-workshop.pdf` | 3 hours | Hands-on | Training sessions, bootcamps |
| `claude-code-interactive-tutorial.pdf` | 2-3 hours | Interactive | Standard workshops |
| `claude-code-tutorial.pdf` | 30 min | Overview | Quick introductions |

## Files Overview

### Presentation Files
- **`ai-first-lecture.pdf`** - 1-hour lecture covering all AI-first topics (NO hands-on)
- **`ai-first-workshop.pdf`** - 3-hour workshop where attendees build from scratch
- **`workshop-prompts.md`** - Prompts for the 3-hour workshop (auto-generated)
- **`claude-code-interactive-tutorial.pdf`** - Original 40+ slide interactive workshop
- **`prompts.md`** - Original workshop prompts with page references
- **`claude-code-tutorial.pdf`** - 17-slide overview presentation (short talks)

### Python Scripts
- **`presentation_utils.py`** - Shared utilities for PDF generation
- **`create_lecture_presentation.py`** - Generates the 1-hour lecture PDF
- **`create_handson_workshop.py`** - Generates the 3-hour workshop PDF + workshop-prompts.md
- **`create_interactive_presentation_v2.py`** - Generates the interactive workshop PDF + prompts.md
- **`create_presentation.py`** - Generates the 17-slide overview PDF

---

## Option 1: 1-Hour Lecture (No Hands-On)

**Use:** `ai-first-lecture.pdf`

### When to Use
- Conference talks
- Team briefings
- Executive presentations
- Introduction sessions without setup time

### Topics Covered (~50 min + Q&A)
1. AI-First Philosophy (4 min)
2. Addressing Common Concerns (5 min)
3. Prompt Engineering vs Vibe Coding (4 min)
4. Getting Started with Prompt Engineering (6 min)
5. Scaling to Large Projects (5 min)
6. Feature Documentation Best Practices (5 min)
7. Testing Strategies (5 min)
8. Project Planning & 10-Step Workflow (4 min)
9. Git Best Practices (4 min)
10. Tips & Tricks (5 min)

### Setup
- Open `ai-first-lecture.pdf` on projector
- No attendee setup needed
- Allow 10-15 min Q&A at end

---

## Option 2: 3-Hour Hands-On Workshop

**Use:** `ai-first-workshop.pdf` + `workshop-prompts.md`

### When to Use
- Full training sessions
- Bootcamps
- Teams wanting practical experience
- Groups with 3+ hours available

### Prerequisites for Attendees
- Laptop with internet
- Claude Code access (or other AI coding assistant)
- Git installed
- GitHub account
- Preferred language runtime (Go, Node, Python)
- Code editor (VS Code, Cursor, etc.)

### Reference Repository
Attendees use `github.com/emmanuelandre/unveiling-claude` as reference (NOT copy-paste).
They build their OWN project from scratch.

### Timeline

| Part | Duration | Content | Hands-On |
|------|----------|---------|----------|
| Part 1 | 20 min | Philosophy & setup | No |
| Part 2 | 30 min | Project setup | Exercises 1-3 |
| Break 1 | 5 min | | |
| Part 3 | 60 min | Build auth feature | Exercises 4-10 |
| Break 2 | 10 min | | |
| Part 4 | 25 min | Testing deep dive | Exercises 11-12 |
| Part 5 | 20 min | Git & best practices | Exercises 13-14 |
| Part 6 | 25 min | Final challenge | Exercise 15 |
| Wrap-up | 5 min | Summary | No |

### Key Exercises
1. Create GitHub repository
2. Create CLAUDE.md project rules
3. Initialize Git workflow
4. Write feature specification
5. Create database schema
6. Implement repository layer
7. Create API handlers
8. Write E2E tests
9. Run and debug tests
10. Add unit tests
11. Create proper commits
12. Push and create PR
13. Final challenge (choose feature)

---

## Option 3: Original Interactive Workshop (2-3 hours)

**Use:** `claude-code-interactive-tutorial.pdf` + `prompts.md`

(See existing guide content below)

## How to Use During Workshop

### Setup (5 minutes before)
1. Open `claude-code-interactive-tutorial.pdf` on projector
2. Ask attendees to open `prompts.md` on their laptops
3. Verify attendees have Claude Code access (claude.ai/code)

### During Workshop
1. **Present slides** - Show slide on projector screen
2. **Reference prompts** - Tell attendees: "See Page X in prompts.md"
3. **Attendees copy/paste** - They copy exact prompts from prompts.md
4. **Live practice** - Everyone types prompts into Claude Code simultaneously
5. **Verify results** - Check that everyone gets expected output

### Prompts File Structure
```markdown
## Page 9: Create Your First Project

**PROMPT:**
```
mkdir my-api-project
cd my-api-project
git init

# Now ask Claude:
Help me create a CLAUDE.md file for a Go API project with:
- PostgreSQL database
- JWT authentication
...
```

**EXPECTED RESULT:**
Claude creates a comprehensive CLAUDE.md with architecture, commands, and conventions
```

## Workshop Flow (2-3 hours)

### Part 1: Philosophy & Foundation (20 min)
- Slides 1-6
- Introduce AI-first development
- No hands-on exercises

### Part 2: Getting Started (30 min)
- Slides 7-10
- **Hands-on**: Pages 9-10 (Create project, Git workflow)
- Attendees set up their first project

### Part 3: AI-First Workflow (60 min)
- Slides 11-25
- **Hands-on**: Pages 13, 15, 17, 19, 21, 22, 24 (Full 10-step process)
- Build complete authentication feature together

### Part 4: Testing Strategy (20 min)
- Slides 26-29
- **Hands-on**: Page 28 (Write E2E test)
- Practice test-driven development

### Part 5: Best Practices (30 min)
- Slides 30-34
- **Hands-on**: Pages 32, 34 (Git workflow, Better prompts)
- Learn proper commit practices

### Part 6: Real-World Application (20 min)
- Slides 35-38
- **Hands-on**: Page 38 (Final exercise)
- 30-minute challenge: Build complete profile feature

### Wrap-up (10 min)
- Slides 39-41
- Q&A
- Share resources

## Tips for Workshop Leaders

### Keep It Interactive
- Pause after each slide with hands-on exercise
- Walk around to help attendees
- Show your screen when demonstrating
- Encourage questions

### Common Issues
1. **Claude not responding** - Check internet connection
2. **Tests failing** - Review error messages together
3. **Attendees falling behind** - Pair them with someone ahead
4. **Prompt confusion** - Show exactly which prompt to use from prompts.md

### Time Management
- Stick to 5-10 min per exercise
- Skip final exercise (page 38) if running short on time
- Can extend Part 3 if attendees are engaged

### What Attendees Need
- Laptop with internet
- Claude Code access (claude.ai/code)
- Code editor (VS Code recommended)
- Git installed
- Go 1.21+ and Node.js 18+ (for exercises)
- Terminal access

## Regenerating Presentations

If you need to update content:

```bash
# Activate virtual environment (required for reportlab)
source .venv/bin/activate

# Generate 1-hour lecture
.venv/bin/python3 create_lecture_presentation.py

# Generate 3-hour workshop + prompts
.venv/bin/python3 create_handson_workshop.py

# Generate original interactive workshop + prompts
.venv/bin/python3 create_interactive_presentation_v2.py

# Generate overview presentation
.venv/bin/python3 create_presentation.py
```

All scripts use `presentation_utils.py` for shared styling and functions.

## Using the Reference Example

The `examples/my-api-project/` directory contains a complete reference implementation.

### What's Included
- `CLAUDE.md` - Production-ready project configuration
- `migrations/001_create_users.up.sql` - Database migration with triggers
- `migrations/001_create_users.down.sql` - Rollback migration

### How to Use During Workshop

1. **Attendees complete exercises independently** first
2. **After each exercise**, show the reference example for comparison
3. **Discuss differences** - different approaches are OK if they work!
4. **Do NOT show before exercise** - prevents learning

### When to Show Reference

| After Exercise | Show |
|----------------|------|
| Page 9 (Create CLAUDE.md) | `examples/my-api-project/CLAUDE.md` |
| Page 15 (Review Schema) | `examples/my-api-project/migrations/` |

### Discussion Points

- Reference CLAUDE.md includes automatic `updated_at` trigger
- Reference migration has both up and down versions
- Compare attendee outputs - different is OK if it works!
- Highlight patterns: indexes, constraints, comments

## Post-Workshop

Share with attendees:
- Full documentation in `/docs` folder
- CLAUDE.md template in `/examples`
- Reference project in `/examples/my-api-project`
- Encourage them to try the final exercise at home

# Workshop Presentation Guide

## Files Overview

### Presentation Files
- **`claude-code-tutorial.pdf`** - 17-slide overview presentation (use for short talks)
- **`claude-code-interactive-tutorial.pdf`** - 40+ slide interactive workshop (full hands-on session)
- **`prompts.md`** - All workshop prompts with page references for easy copy-paste

### Python Scripts
- **`create_presentation.py`** - Generates the 17-slide overview PDF
- **`create_interactive_presentation_v2.py`** - Generates the interactive workshop PDF and prompts.md

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
# Update the overview presentation
python3 create_presentation.py

# Update the interactive workshop + prompts
python3 create_interactive_presentation_v2.py
```

Both commands generate PDFs. The v2 script also generates `prompts.md`.

## Post-Workshop

Share with attendees:
- Full documentation in `/docs` folder
- CLAUDE.md template in `/examples`
- Encourage them to try the final exercise at home

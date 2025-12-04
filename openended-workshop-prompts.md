# AI-First Open-Ended Workshop Prompts

Copy and paste these prompts during the workshop exercises.

---

## Page 14: Exercise 1: Browse & Choose Your Project

**PROMPT:**
```
Go to: github.com/emmanuelandre/unveiling-claude

Browse the available projects:
- manu-code/ - AI CLI assistant (High complexity)
- task-manager/ - Task management API (Medium)
- my-api-project/ - Simple API starter (Low)
- prompt-ops/ - Prompt operations (Medium)
- ui-to-test/ - UI testing (Medium)

Read the specs and choose ONE project.

OR: Come up with your own idea!

When ready, raise your hand to share your choice.
```

**EXPECTED RESULT:**
You've chosen a project and have a rough idea of what to build

---

## Page 16: Exercise 2: Initial Setup

**PROMPT:**
```
Choose ONE option:

OPTION A: Fork unveiling-claude (if using sample project)
1. Go to github.com/emmanuelandre/unveiling-claude
2. Click "Fork" to create your copy
3. Clone your fork:
   git clone https://github.com/[YOUR-USERNAME]/unveiling-claude.git
   cd unveiling-claude/[your-project]

OPTION B: Create new repo (if using own idea)
1. Create new repo on GitHub
2. Clone it locally:
   git clone https://github.com/[YOUR-USERNAME]/[your-repo].git
   cd [your-repo]
   git checkout -b feature/initial-setup

Open your AI assistant and get ready!
```

**EXPECTED RESULT:**
Repository set up and ready to work

---

## Page 20: Exercise 3: Create Your Plan with AI

**PROMPT:**
```
Tell your AI assistant:

I want to build [PROJECT NAME].

Project context: [Brief description or link to spec]

Help me create:
1. A CLAUDE.md (or project rules file) with:
   - Project overview
   - Tech stack
   - Project structure
   - Commands (build, test, run)
   - Testing requirements

2. A specification for the FIRST feature I should build
   - Keep it scoped for ~60 min implementation
   - Include success criteria

3. A rough implementation plan

My tech stack preference: [Go/Node/Python/TypeScript]
```

**EXPECTED RESULT:**
CLAUDE.md created and first feature specified

---

## Page 26: Exercise 4: Implementation Sprint 1

**PROMPT:**
```
Time to build! Follow your plan.

Suggested approach:
1. Start with data layer (database schema, models)
2. Then business logic (repository, handlers)
3. Then tests

Example prompt to start:
"Based on our spec, let's start implementing.
First, create the database schema for [your feature].
Include proper types, indexes, and constraints."

Continue from there. Work at your own pace.

Checkpoint in 35 minutes!
```

**EXPECTED RESULT:**
Core feature partially or fully implemented

---

## Page 30: Exercise 5: Implementation Sprint 2

**PROMPT:**
```
Continue building your feature.

Focus on:
- Completing what you started
- Adding tests for what works
- Making it demo-able

If you finished early:
- Add another small feature
- Improve tests
- Clean up code
- Help a neighbor

Remember: Something working > Something perfect

Checkpoint in 25 minutes - prepare for demo!
```

**EXPECTED RESULT:**
Feature implemented and ready to demo

---

## Page 34: Exercise 6: Commit and Push

**PROMPT:**
```
Commit and push your work:

1. Review changes:
   git status
   git diff

2. Stage and commit:
   git add .
   git commit -m "feat([scope]): [what you built]

   - [Key thing 1]
   - [Key thing 2]
   - [Key thing 3]"

3. Push:
   git push origin [your-branch]

4. (Optional) Create PR:
   gh pr create --title "feat: [your feature]" \
     --body "## What I Built
   [Description]

   ## What Works
   - [Feature 1]
   - [Feature 2]"

Or create PR through GitHub web interface.
```

**EXPECTED RESULT:**
Code committed and pushed to GitHub

---


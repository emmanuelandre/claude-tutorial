# Quick Start Guide

Get productive with Claude Code in 5 minutes.

## Prerequisites

- Git installed
- Basic command line knowledge
- A code editor (VS Code recommended)
- Claude Code access (claude.ai/code)

## Step 1: Create Your Project

```bash
mkdir my-project
cd my-project
git init
```

## Step 2: Create CLAUDE.md

The CLAUDE.md file is your project's instruction manual for Claude.

```bash
cat > CLAUDE.md << 'EOF'
# My Project

## Overview
[Brief description of your project]

## Tech Stack
- Language: [e.g., Python, Go, JavaScript]
- Framework: [e.g., FastAPI, Express, React]
- Database: [e.g., PostgreSQL, MongoDB]

## Development Workflow

### Git Workflow
- Branch naming: `<type>/<description>`
  - Types: feature, fix, refactor, docs, test
- Commit format: `<type>(<scope>): <message>`
- Never commit directly to main
- Create PR for all changes

### Code Standards
- Run linter before commit
- Run tests before commit
- Add tests for new features
- Update documentation

## Project Structure
```
my-project/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
└── README.md      # Project overview
```

## Commands
```bash
# Install dependencies
[your install command]

# Run tests
[your test command]

# Start development server
[your dev server command]
```
EOF
```

## Step 3: Start Your First Session

Open Claude Code and start with a clear goal:

```
"I'm starting a new [type] project. Based on my CLAUDE.md,
please help me:
1. Set up the basic project structure
2. Create a hello world endpoint/feature
3. Add tests for it
4. Set up linting and formatting"
```

## Step 4: Validate & Iterate

After Claude implements:

1. **Review the code** - Understand what was created
2. **Run tests** - Ensure everything works
3. **Try the feature** - Manual testing
4. **Request changes** - Refine as needed

## Step 5: Commit Your Work

```bash
# Review changes
git status
git diff

# Create feature branch
git checkout -b feature/initial-setup

# Stage and commit
git add .
git commit -m "feat: initial project setup"

# Push to remote
git push origin feature/initial-setup
```

## Next Steps

✅ **You now have:**
- Project initialized
- CLAUDE.md configured
- First feature implemented
- Tests passing
- Code committed

**Continue to:**
- [The CLAUDE.md File](./04-claude-md.md) - Deep dive into configuration
- [Feature Workflow](./08-feature-workflow.md) - Full development cycle
- [Best Practices](./11-git-workflow.md) - Team standards

---

**Prev:** [Introduction](./01-introduction.md) | **Next:** [Setup Guide](./03-setup-guide.md)

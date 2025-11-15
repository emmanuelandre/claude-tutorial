# Setup Guide

Complete setup for Claude Code development.

## Prerequisites

### Required
- **Git** 2.x or higher
- **Code Editor** (VS Code, Cursor, or similar)
- **Claude Code Access** at claude.ai/code
- **Terminal** knowledge (basic commands)

### Optional
- **GitHub CLI** (`gh`) for PR management
- **Docker** if working with containers
- **Language-specific tools** (Node.js, Python, Go, etc.)

## Initial Setup

### 1. Install Git

**macOS:**
```bash
brew install git
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install git
```

**Windows:**
Download from git-scm.com

### 2. Configure Git

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Default branch name
git config --global init.defaultBranch main

# Better defaults
git config --global pull.rebase true
git config --global fetch.prune true
```

### 3. Set Up SSH Keys (Recommended)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

### 4. Install GitHub CLI (Optional)

**macOS:**
```bash
brew install gh
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

**Authenticate:**
```bash
gh auth login
```

## Project Setup

### Starting a New Project

```bash
# Create project directory
mkdir my-project
cd my-project

# Initialize git
git init

# Create CLAUDE.md
touch CLAUDE.md
```

### Joining an Existing Project

```bash
# Clone repository
git clone git@github.com:username/repo.git
cd repo

# Install dependencies (example for Node.js)
npm install

# Or for Python
pip install -r requirements.txt

# Or for Go
go mod download
```

## CLAUDE.md Configuration

Create a CLAUDE.md file at your project root:

```markdown
# Project Name

## Overview
Brief description of what this project does.

## Tech Stack
- Language/Framework
- Database
- Key dependencies

## Development Workflow

### Git Workflow
- Branch naming: `<type>/<description>`
- Commit format: `<type>(<scope>): <message>`
- Never commit directly to main

### Code Standards
- Run linter before commit
- Run tests before commit
- Add tests for new features

## Project Structure
```
project/
├── src/
├── tests/
└── docs/
```

## Common Commands
```bash
# Development
[command to run dev server]

# Testing
[command to run tests]

# Build
[command to build]
```
```

See [The CLAUDE.md File](./04-claude-md.md) for detailed configuration.

## Language-Specific Setup

### Node.js/JavaScript

```bash
# Install Node.js (via nvm recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
nvm use --lts

# Verify
node --version
npm --version

# Initialize project
npm init -y

# Install common tools
npm install -D eslint prettier jest
```

### Python

```bash
# Install Python 3.10+
# macOS
brew install python@3.11

# Ubuntu
sudo apt-get install python3.11 python3.11-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Go

```bash
# Install Go
# macOS
brew install go

# Ubuntu
sudo snap install go --classic

# Verify
go version

# Initialize module
go mod init github.com/username/project

# Download dependencies
go mod download
```

## Editor Configuration

### VS Code

**Recommended Extensions:**
- ESLint (JavaScript/TypeScript)
- Prettier
- GitLens
- Python (if using Python)
- Go (if using Go)

**Settings (`.vscode/settings.json`):**
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "eslint.validate": ["javascript", "typescript"],
  "files.trimTrailingWhitespace": true
}
```

### Cursor

Cursor works similarly to VS Code with built-in AI features.

## Testing Your Setup

### 1. Create Test File

```bash
# JavaScript
echo "console.log('Hello World');" > test.js
node test.js

# Python
echo "print('Hello World')" > test.py
python test.py

# Go
echo 'package main; import "fmt"; func main() { fmt.Println("Hello World") }' > test.go
go run test.go
```

### 2. Test Git

```bash
# Check status
git status

# Create test commit
echo "# Test" > TEST.md
git add TEST.md
git commit -m "test: verify git setup"
```

### 3. Test GitHub CLI (if installed)

```bash
# Check authentication
gh auth status

# List repos
gh repo list
```

## Troubleshooting

### Git Permission Denied

```bash
# Check SSH connection
ssh -T git@github.com

# Should see: "Hi username! You've successfully authenticated"
```

### Python Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node.js Permission Errors

```bash
# Use nvm instead of system Node.js
# Avoid using sudo with npm
```

### Go Module Issues

```bash
# Clear module cache
go clean -modcache

# Re-download dependencies
go mod download
```

## Next Steps

✅ **You now have:**
- Git configured
- Editor ready
- Language tools installed
- Project initialized
- CLAUDE.md created

**Continue to:**
- [The CLAUDE.md File](./04-claude-md.md) - Configure your project
- [Prompt Engineering](./05-prompt-engineering.md) - Learn effective prompting
- [Feature Workflow](./08-feature-workflow.md) - Start building

---

**Prev:** [Quick Start](./02-quick-start.md) | **Next:** [The CLAUDE.md File](./04-claude-md.md)

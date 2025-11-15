# Git Workflow Best Practices

## Branch Naming Convention

```
<type>/<short-description>
```

### Types
- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `refactor/` - Code refactoring without functionality changes
- `docs/` - Documentation changes
- `test/` - Test additions or modifications
- `chore/` - Maintenance tasks (dependencies, tooling)
- `perf/` - Performance improvements

### Examples
```
feature/user-authentication
fix/login-redirect-loop
refactor/extract-auth-middleware
docs/update-api-documentation
test/add-checkout-e2e-tests
chore/upgrade-dependencies
```

## Commit Message Format

Follow **Conventional Commits** (conventionalcommits.org):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
`feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`, `perf`, `ci`, `build`

### Examples
```
feat(auth): add Google OAuth login
fix(api): resolve race condition in token refresh
refactor(db): extract query builder into utility
docs: update deployment guide
test(checkout): add E2E tests for payment flow
```

### Important Rules

✅ **DO:**
- Use imperative mood ("add" not "added")
- Be concise but descriptive
- Include scope when relevant
- Reference issue numbers in footer

❌ **DON'T:**
- Add "Co-Authored-By" or AI attribution
- Use emojis in commit messages
- Write vague messages ("fix bug", "update code")
- Commit directly to main/master

## Workflow Steps

### 1. Create Branch
```bash
# Always start from updated main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/user-roles
```

### 2. Make Changes
- Write code
- Add tests
- Update documentation

### 3. Pre-Commit Checks

**Critical**: Run these BEFORE every commit:

```bash
# Format code
npm run format  # or: go fmt ./...

# Run linter
npm run lint    # or: golangci-lint run

# Run tests
npm test        # or: go test ./...

# Build
npm run build   # or: go build ./...
```

**If any check fails, fix it before committing.**

### 4. Commit Changes
```bash
# Stage changes
git add .

# Commit with conventional message
git commit -m "feat(roles): add RBAC with 3 role types"
```

### 5. Push Branch
```bash
# First push
git push -u origin feature/user-roles

# Subsequent pushes
git push
```

### 6. Create Pull Request

Use GitHub CLI or web interface:

```bash
# Using gh CLI
gh pr create --title "feat: Add user roles with RBAC" \
  --body "## Summary
Implements role-based access control with 3 roles:
- Admin (full access)
- Editor (read/write)
- Viewer (read only)

## Changes
- Database migration for roles table
- RBAC middleware
- Permission checking utilities
- E2E tests for all roles

## Testing
- All E2E tests pass
- Manual testing completed
- No breaking changes"
```

### 7. Code Review

**Three-Layer Review:**
1. **You** - Self-review before requesting
2. **Peer** - Team member review
3. **AI** - Automated checks + AI code review

**Review Checklist:**
- ✅ Code follows project conventions
- ✅ Tests are comprehensive
- ✅ Documentation is updated
- ✅ No security issues
- ✅ Performance impact considered
- ✅ Breaking changes documented

### 8. Merge (Human Only)

**Never let AI merge PRs.**

After approval:
```bash
# Squash merge (preferred for clean history)
gh pr merge --squash

# Or use GitHub web interface
```

### 9. Cleanup
```bash
# Delete local branch
git checkout main
git pull
git branch -d feature/user-roles

# Remote branch deleted automatically by GitHub
```

## PR Best Practices

### Size
- ✅ Small: 100-300 lines changed
- ⚠️ Medium: 300-500 lines
- ❌ Large: 500+ lines (split into multiple PRs)

### Description Template
```markdown
## Summary
[What this PR does]

## Changes
- [List of changes]

## Testing
- [How it was tested]

## Screenshots (if UI changes)
[Add screenshots]

## Breaking Changes
[List any breaking changes]

## Related Issues
Closes #123
Relates to #456
```

### Handling Feedback
```bash
# Make requested changes
# ... edit files ...

# Commit changes
git add .
git commit -m "refactor: apply review feedback"
git push

# PR automatically updates
```

## Common Scenarios

### Rebase on Main
```bash
# Update your branch with latest main
git checkout feature/my-feature
git fetch origin
git rebase origin/main

# Resolve conflicts if any
# ... fix conflicts ...
git add .
git rebase --continue

# Force push (branch is already remote)
git push --force-with-lease
```

### Fix Commit Message
```bash
# Last commit only
git commit --amend -m "feat(auth): add OAuth support"
git push --force-with-lease

# Older commits (use interactive rebase)
git rebase -i HEAD~3
# Change "pick" to "reword" for commits to fix
# Save and edit messages
git push --force-with-lease
```

### Stash Changes
```bash
# Save work in progress
git stash save "WIP: implementing user roles"

# Switch branches
git checkout main

# Return and restore
git checkout feature/user-roles
git stash pop
```

## Rules and Policies

### Hard Rules (Never Break)
1. **Never commit directly to main**
2. **Never merge your own PR without review**
3. **Never commit code that fails tests**
4. **Never commit secrets or credentials**
5. **Never force push to main**

### Soft Rules (Follow Unless Exception)
1. Commit messages follow conventional format
2. PRs include tests for new code
3. PRs update relevant documentation
4. Branches deleted after merge
5. Commits are atomic (one logical change)

### AI-Specific Rules
1. ❌ AI cannot merge PRs
2. ❌ AI cannot approve PRs
3. ✅ AI can create branches
4. ✅ AI can commit code
5. ✅ AI can push branches
6. ✅ AI can open PRs

## Git Configuration

### Recommended Settings
```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Default branch name
git config --global init.defaultBranch main

# Rebase by default when pulling
git config --global pull.rebase true

# Prune deleted remote branches
git config --global fetch.prune true

# Use better diff algorithm
git config --global diff.algorithm histogram
```

### Useful Aliases
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --graph --oneline --all"
```

## Summary

**Key Takeaways:**
- Clear branch naming and commit conventions
- Pre-commit checks are mandatory
- Small, focused PRs
- Three-layer review process
- Humans merge, AI executes

---

**Next:** [Documentation Strategies](./12-documentation.md)

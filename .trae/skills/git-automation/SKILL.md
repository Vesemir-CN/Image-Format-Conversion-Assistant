---
name: "git-automation"
description: "Automates Git operations (commit, PR, merge). Invoke when user wants to automate Git workflow."
---

# Git Automation Skill

This skill helps automate Git operations including commits, branches, and pull requests.

## Git Operations

### Check Status
```bash
git status
git diff
git log --oneline -10
```

### Create CommitConventional Commits)
```bash
# Stage ( all changes
git add -A

# Create commit with conventional format
git commit -m "feat: add new feature"
# Types: feat, fix, docs, style, refactor, test, chore
```

### Branch Operations
```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Push branch
git push -u origin feature/new-feature
```

### Pull Request
```bash
# Create PR (GitHub CLI)
gh pr create --title "Feature Name" --body "Description"

# Or use Git
git push --set-upstream origin feature/xxx
```

## Conventional Commits Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Formatting
- **refactor**: Code restructuring
- **test**: Testing
- **chore**: Maintenance

## Best Practices

1. Write meaningful commit messages
2. Use conventional commits format
3. Commit often with small changes
4. Pull before push
5. Review before merge

## Usage

Invoke this skill when user wants to:
- Create Git commits
- Manage branches
- Create pull requests
- Follow Git workflow
- Automate Git operations

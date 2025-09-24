---
allowed-tools: Bash(git:*), Bash(gh:*)
description: Sync repository with remote and update dependencies
---

## Current State
- Branch: !`git branch --show-current`
- Status: !`git status -sb | head -1`
- Stashes: !`git stash list | wc -l`

## Task

Sync repository:

1. Stash local changes if any
2. Fetch all remotes
3. Update main/develop branches
4. Rebase current branch if needed
5. Update git submodules
6. Install new dependencies
7. Run migrations if any
8. Pop stashed changes

For Python projects:
```bash
pip install -r requirements.txt
pip install -e .
```

For Phase 1 specific:
- Check for config changes
- Verify Firebase credentials
- Update hardware libraries
- Test serial port access

Show summary of:
- New commits pulled
- Files updated
- Dependencies changed
- Migration status
---
allowed-tools: Bash(git:*)
argument-hint: [branch-name]
description: Switch branches with safety checks
---

## Current Status
- Current branch: !`git branch --show-current`
- Modified files: !`git status --porcelain | wc -l`
- Stash count: !`git stash list | wc -l`

## Task

Switch to branch: $1

Safety checks:
1. Check for uncommitted changes
2. Offer to stash if needed
3. Pull latest changes after switch
4. Show branch history summary
5. List TODOs or FIXMEs in branch

If switching to develop/main:
- Ensure branch is up to date with origin
- Show recent merge history
- Check CI/CD status
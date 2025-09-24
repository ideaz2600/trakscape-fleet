---
allowed-tools: Bash(git:*), Bash(gh:*)
description: Clean up merged and stale branches
---

## Branch Status
- Local branches: !`git branch | wc -l`
- Remote branches: !`git branch -r | wc -l`
- Merged branches: !`git branch --merged | grep -v "\*\|main\|develop" | wc -l`

## Task

Clean up branches:

1. List branches merged into main/develop
2. Delete local merged branches
3. Identify stale branches (>30 days)
4. Check for branches with closed issues
5. Prune remote tracking branches
6. Archive feature branches if needed

Keep:
- main/master
- develop
- Active release branches
- Current working branch

Show summary of cleaned branches.
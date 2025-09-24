---
allowed-tools: Bash(gh:*), Bash(git:*)
argument-hint: [issue-number] [reason]
description: Close an issue with resolution notes
---

## Task

Close issue #$1 with reason: $2

Steps:
1. Add a comment explaining the resolution
2. Close the issue with appropriate label (resolved/wont-fix/duplicate)
3. Link any related PRs or commits
4. Update project board status

If the issue is part of Phase 1, ensure:
- Related tasks are updated
- Documentation is complete
- Tests are passing
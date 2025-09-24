---
allowed-tools: Bash(gh:*)
argument-hint: [issue-number] [assignee]
description: Assign an issue to a team member
---

## Task

Assign issue #$1 to $2

Actions:
1. Update issue assignee
2. Add comment notifying assignment
3. Update issue labels if needed (in-progress)
4. Check for blocking dependencies

For Phase 1 hardware integration issues:
- Verify hardware component availability
- Check for related configuration tasks
- Link to relevant documentation
---
allowed-tools: Bash(gh:*)
argument-hint: [type] [title] [description]
description: Create a new GitHub issue with proper labeling
---

## Current Status
- Current branch: !`git branch --show-current 2>/dev/null || echo "main"`
- Repository status: !`gh repo view --json name,description 2>/dev/null || echo "Not connected to GitHub"`

## Task

Create a new GitHub issue based on the following parameters:
- Issue type: $1 (bug/feature/task/enhancement)
- Title: $2
- Description: $3

Apply appropriate labels based on the type:
- bug → labels: bug, priority-high
- feature → labels: enhancement, phase-1
- task → labels: task, documentation
- enhancement → labels: enhancement, improvement

For Phase 1 fleet tracking issues, also add:
- Milestone: "Phase 1 - Core GPS Tracking"
- Project: "Trakscape Fleet Platform"
- Assignee: Current user

Use gh cli to create the issue and return the issue number and URL.
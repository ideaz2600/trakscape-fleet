---
allowed-tools: Bash(git:*), Bash(gh:*), TodoWrite, Read
argument-hint: [issue-number]
description: Start working on a feature from a GitHub issue
---

## Issue Details
- Issue info: !`gh issue view $1 --json title,body,labels,assignees,milestone`
- Issue URL: !`gh issue view $1 --json url -q .url`

## Task

Start feature from Issue #$1

Complete feature setup:
1. Parse issue title to create branch name (feature/issue-$1-<sanitized-title>)
2. Create feature branch from develop
3. Update issue status to "In Progress"
4. Set up local development environment based on issue labels
5. Create initial project structure from issue description
6. Extract TODO items from issue body
7. Create draft PR linked to issue

For Phase 1 Fleet Tracker features (based on issue labels):
- GPS Tracking: Set up serial communication testing
- Firebase Sync: Configure credentials and project
- UPS Management: Enable I2C interface
- Data Buffer: Initialize SQLite database

Project structure to create:
```
src/
  features/
    $1/
      __init__.py
      implementation.py
      tests/
        test_$1.py
      docs/
        README.md
```

Auto-generate from issue:
- Feature branch name from issue title
- Implementation tasks from issue description
- Test cases from acceptance criteria
- Documentation requirements

Update issue with:
- Branch name and PR link
- Development progress
- Blockers or dependencies
- Estimated completion date

Link PR to issue using:
- "Closes #$1" in PR description
- GitHub auto-link references
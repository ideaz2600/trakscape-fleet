---
allowed-tools: Bash(git:*), Bash(gh:*), TodoWrite, Read, Task, Write, Edit, MultiEdit
argument-hint: [issue-number]
description: Start working on a feature from a GitHub issue with specialized subagent support
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

## Utilize Specialized Subagents

Based on the issue labels and content, delegate to appropriate specialist subagents:

- **GPS/4G HAT features**: Use the gps-hat-specialist subagent for serial AT commands, GPS parsing, and cellular connectivity
- **Firebase features**: Use the firebase-specialist subagent for real-time database, offline sync, and batch uploads
- **Power/UPS features**: Use the ups-power-specialist subagent for I2C communication, battery monitoring, and shutdown procedures
- **Deployment tasks**: Use the pi-deployment-specialist subagent for Raspberry Pi setup and systemd services
- **Testing requirements**: Use the test-validator-specialist subagent for unit tests, mocks, and integration tests
- **Overall coordination**: Use the fleet-project-orchestrator subagent to coordinate multiple specialists

For Phase 1 Fleet Tracker features (based on issue labels):
- GPS Tracking: Delegate to gps-hat-specialist for serial communication setup
- Firebase Sync: Delegate to firebase-specialist for credentials and project config
- UPS Management: Delegate to ups-power-specialist for I2C interface setup
- Data Buffer: Delegate to firebase-specialist for SQLite database initialization

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
---
allowed-tools: Bash(gh:*)
argument-hint: [filter]
description: List GitHub issues with optional filtering
---

## Current Repository
- Repo: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "Not connected"`
- Open issues count: !`gh issue list --state open --json number | jq length 2>/dev/null || echo "0"`

## Task

List GitHub issues with filter: $ARGUMENTS

Filter options:
- all: Show all issues
- open: Show open issues (default)
- closed: Show closed issues  
- phase1: Show Phase 1 related issues
- mine: Show issues assigned to me
- unassigned: Show unassigned issues

Display format:
1. Issue number and title
2. Status, labels, assignee
3. Created date and last updated
4. Linked PR if any

Group by milestone when applicable.
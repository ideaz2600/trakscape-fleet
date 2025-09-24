---
allowed-tools: Bash(git:*), Bash(gh:*)
argument-hint: [feature-name] [issue-number]
description: Create a new feature branch following Git Flow
---

## Current State
- Current branch: !`git branch --show-current 2>/dev/null || echo "No repo"`
- Uncommitted changes: !`git status --porcelain 2>/dev/null | wc -l`

## Task

Create feature branch: feature/$1
Linked to issue: #$2

Steps:
1. Ensure on develop branch and up to date
2. Create branch: feature/$1-issue-$2
3. Push branch with upstream tracking
4. Update issue #$2 with branch information
5. Set up PR draft if requested

Naming conventions for Phase 1 features:
- feature/gps-tracking-issue-X
- feature/firebase-sync-issue-X
- feature/ups-management-issue-X
- feature/cellular-connection-issue-X

Ensure working directory is clean before branching.
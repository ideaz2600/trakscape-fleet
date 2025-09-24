---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(python:*)
argument-hint: [feature-name]
description: Complete and merge a feature
---

## Pre-merge Checklist
- Tests status: !`python -m pytest 2>/dev/null || echo "No tests"`
- Linting: !`pylint src/ 2>/dev/null || echo "Linter not configured"`
- Branch status: !`git status --porcelain`

## Task

Finish feature: $1

Completion steps:
1. Run all tests and ensure passing
2. Update documentation
3. Squash commits if needed
4. Update CHANGELOG.md
5. Mark PR ready for review
6. Request reviewers
7. Merge to develop after approval
8. Delete feature branch
9. Close related issue(s)

Phase 1 specific checks:
- Hardware integration tested on Pi
- Power consumption documented
- Offline capability verified
- Firebase sync confirmed
- Error handling comprehensive
- Logging implemented

Post-merge:
- Update project board
- Notify team
- Plan next feature
---
allowed-tools: Bash(gh:*), Bash(git:*), Read, Grep
argument-hint: [pr-number]
description: Review a feature PR thoroughly
---

## PR Information
- PR details: !`gh pr view $1 --json title,state,author`
- Files changed: !`gh pr diff $1 --name-only | wc -l`
- Comments: !`gh pr view $1 --json comments | jq '.comments | length'`

## Task

Review PR #$1

Review checklist:
1. Code quality and style
2. Test coverage
3. Documentation updates
4. Performance implications
5. Security considerations
6. Hardware compatibility (Pi specific)
7. Error handling
8. Logging adequacy

Phase 1 Fleet Tracker focus areas:
- GPS data accuracy
- Cellular data usage optimization
- Power efficiency
- Offline resilience
- Firebase quota usage
- Memory footprint on Pi

Provide feedback on:
- Potential bugs
- Optimization opportunities  
- Missing edge cases
- Documentation gaps
- Testing improvements

Create review with approve/request-changes/comment.
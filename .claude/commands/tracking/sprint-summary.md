---
allowed-tools: Bash(gh:*), Bash(git:*)
argument-hint: [sprint-number]
description: Generate sprint summary and metrics
---

## Current Sprint
- Sprint: $1
- Active issues: !`gh issue list --label "sprint-$1" --state open --json number | jq length`
- Completed: !`gh issue list --label "sprint-$1" --state closed --json number | jq length`

## Task

Generate Sprint $1 summary:

### Sprint Goals
- Review original sprint objectives
- Track completion percentage
- Identify carried-over items

### Velocity Metrics
- Story points completed
- Issues closed
- PRs merged
- Code changes (insertions/deletions)

### Phase 1 Component Progress

**GPS Tracking:**
- [Status] Serial communication
- [Status] NMEA parsing
- [Status] Location accuracy testing

**Firebase Integration:**
- [Status] Authentication setup
- [Status] Real-time database schema
- [Status] Offline sync queue

**UPS Management:**
- [Status] I2C communication
- [Status] Battery monitoring
- [Status] Shutdown procedures

**Data Buffer:**
- [Status] SQLite schema
- [Status] Queue implementation
- [Status] Cleanup routines

### Blockers & Risks
- List critical blockers
- Hardware dependencies
- External API issues
- Team capacity constraints

### Next Sprint Planning
- Carryover items
- New priorities
- Resource allocation
- Dependencies resolution
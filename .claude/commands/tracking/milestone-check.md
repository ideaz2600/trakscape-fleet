---
allowed-tools: Bash(gh:*)
argument-hint: [milestone-name]
description: Check milestone progress and timeline
---

## Milestone Status
- Milestone: !`gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.title=="$1") | "\(.title): \(.open_issues) open, \(.closed_issues) closed"' 2>/dev/null`
- Due date: !`gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.title=="$1") | .due_on' 2>/dev/null`

## Task

Analyze milestone: $1

### Milestone Overview
1. Total issues assigned
2. Completion percentage
3. Days remaining
4. Burn-down rate
5. Projected completion date

### Phase 1 Milestones

**Core GPS Tracking:**
- Hardware setup complete
- GPS module integration
- Data parsing implementation
- Accuracy validation

**Cellular Connectivity:**
- 4G HAT configuration
- Network management
- Data optimization
- Connection resilience

**Firebase Backend:**
- Project setup
- Schema design
- Authentication
- Real-time sync

**Power Management:**
- UPS integration
- Battery monitoring
- Graceful shutdown
- Power optimization

### Critical Path Analysis
- Identify dependencies
- Show blocking issues
- Resource constraints
- Risk mitigation needed

### Recommendations
- Priority adjustments
- Resource reallocation
- Scope modifications
- Timeline updates
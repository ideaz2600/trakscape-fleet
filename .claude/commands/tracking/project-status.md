---
allowed-tools: Bash(gh:*), Bash(git:*)
description: Show comprehensive project status
---

## Repository Status
- Current branch: !`git branch --show-current`
- Uncommitted changes: !`git status --porcelain | wc -l`
- Commits ahead/behind: !`git status -sb | head -1`

## GitHub Project Status
- Open issues: !`gh issue list --state open --json number | jq length`
- Open PRs: !`gh pr list --state open --json number | jq length`
- Milestone progress: !`gh api repos/{owner}/{repo}/milestones --jq '.[0] | "\(.title): \(.open_issues)/\(.closed_issues) closed"' 2>/dev/null || echo "No milestones"`

## Task

Generate comprehensive project status report:

### Phase 1 Progress
1. List all Phase 1 issues (open/closed)
2. Show PR status for each component:
   - GPS Tracking module
   - Firebase integration
   - UPS power management
   - Data buffering system

### Development Metrics
- Lines of code added this week
- Test coverage percentage
- Open bugs vs features
- Average PR review time
- Deployment frequency

### Team Activity
- Recent commits (last 7 days)
- Active branches
- Pending reviews
- Blocked issues

### Hardware Testing Status
- Components verified
- Integration tests passed
- Performance benchmarks
- Known hardware issues

### Next Sprint Planning
- High priority items
- Dependencies
- Resource requirements
- Risk assessment

Format as markdown table for dashboard display.
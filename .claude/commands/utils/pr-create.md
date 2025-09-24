---
allowed-tools: Bash(gh:*), Bash(git:*)
argument-hint: [title] [issue-number]
description: Create a pull request with template
---

## Branch Info
- Current branch: !`git branch --show-current`
- Commits ahead: !`git rev-list --count origin/develop..HEAD 2>/dev/null || echo "0"`
- Files changed: !`git diff --name-only origin/develop 2>/dev/null | wc -l`

## Task

Create PR: $1
Linked to issue: #$2

### PR Template

#### Description
Brief description of changes

#### Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

#### Phase 1 Component
- [ ] GPS Tracking
- [ ] Firebase Sync
- [ ] UPS Management
- [ ] Data Buffer
- [ ] Core Infrastructure

#### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Hardware tested on Pi
- [ ] Manual testing completed

#### Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data exposed
- [ ] Dependency versions pinned

#### Performance Impact
- Memory usage: 
- CPU impact:
- Network usage:
- Battery impact:

#### Screenshots/Logs
(if applicable)

#### Related Issues
Closes #$2

Create PR with:
- Auto-assign reviewers
- Add appropriate labels
- Link to project board
- Set milestone
---
allowed-tools: Bash(git:*)
argument-hint: [commit-type] [scope] [message]
description: Create a conventional commit
---

## Working Directory
- Modified files: !`git status --porcelain | grep "^ M" | wc -l`
- Untracked files: !`git status --porcelain | grep "^??" | wc -l`
- Staged files: !`git diff --cached --name-only | wc -l`

## Task

Create commit:
Type: $1 (feat/fix/docs/refactor/test/chore)
Scope: $2 (gps/firebase/ups/buffer/core)
Message: $3

Commit format:
```
$1($2): $3

- Detailed description
- What changed and why
- Any breaking changes

Related to #issue-number
```

Conventional commit types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Test additions/changes
- chore: Build/tooling changes
- perf: Performance improvements

Phase 1 scopes:
- gps: GPS tracking module
- firebase: Firebase sync
- ups: Power management
- buffer: Data buffering
- core: Core infrastructure
- config: Configuration
- deploy: Deployment

Pre-commit checks:
1. Run linting
2. Run tests
3. Check for secrets
4. Verify imports
5. Stage all changes
6. Create commit
7. Show commit summary
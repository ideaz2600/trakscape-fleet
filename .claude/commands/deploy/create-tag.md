---
allowed-tools: Bash(git:*), Bash(gh:*)
argument-hint: [version] [message]
description: Create and push a version tag
---

## Task

Create tag: v$1
Message: $2

Tagging process:
1. Ensure on correct branch (main/master)
2. Verify all tests pass
3. Create annotated tag
4. Include release notes
5. Push tag to origin
6. Create GitHub release
7. Attach artifacts

Tag message format:
```
Release v$1

$2

Phase 1 Features:
- GPS tracking implementation
- Firebase real-time sync
- UPS power management
- Offline data buffering

Tested on:
- Raspberry Pi 5 (8GB)
- 4G LTE HAT
- UPS HAT
```

Generate release artifacts:
- Source code archive
- Deployment package
- Configuration templates
- Installation guide
---
allowed-tools: Bash(git:*), Bash(gh:*)
argument-hint: [hotfix-name] [issue-number]
description: Create emergency hotfix branch from main
---

## Task

Create hotfix branch: hotfix/$1 for issue #$2

Hotfix workflow:
1. Create branch from main/master
2. Name: hotfix/$1-issue-$2
3. Apply minimal fix
4. Test thoroughly
5. Merge to main AND develop

For fleet tracker critical fixes:
- GPS signal loss handling
- Firebase connection failures  
- Power management crashes
- Data corruption issues

Create PR targeting both main and develop branches.
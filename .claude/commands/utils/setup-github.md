---
allowed-tools: Bash(gh:*), Bash(git:*)
description: Create GitHub repository and configure remote
---

## Task

Set up GitHub repository for Trakscape Fleet Platform

Steps:
1. Create repository on GitHub
2. Add remote origin
3. Push initial commit
4. Set up branch protection
5. Configure repository settings

Create repository with:
```bash
gh repo create trakscape-fleet --public --description "Real-time GPS fleet tracking system for Raspberry Pi" --clone=false
```

Then configure:
```bash
git remote add origin https://github.com/$(gh api user -q .login)/trakscape-fleet.git
git push -u origin main
```

Set up:
- Branch protection for main
- Issue templates
- PR templates
- GitHub Actions for CI/CD
---
allowed-tools: Bash(git:*), Bash(gh:*), Write
argument-hint: [version] [release-type]
description: Prepare a new release from develop
---

## Current State
- Latest tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags"`
- Commits since last release: !`git rev-list --count $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD)..HEAD`

## Task

Prepare release: v$1
Type: $2 (major/minor/patch/beta)

Release preparation:
1. Create release branch: release/v$1
2. Update version in:
   - setup.py / pyproject.toml
   - __version__.py files
   - README.md
3. Generate CHANGELOG from commits
4. Run full test suite
5. Build deployment package
6. Create release notes

Phase 1 Release Checklist:
- [ ] GPS tracking functional
- [ ] Firebase sync operational  
- [ ] UPS management tested
- [ ] Offline mode verified
- [ ] System service configured
- [ ] Documentation complete
- [ ] Hardware setup guide updated
- [ ] Performance benchmarks documented

Deployment package contents:
- Python wheel/package
- Systemd service files
- Configuration templates
- Installation script
- Hardware test utilities
---
allowed-tools: Bash(ssh:*), Bash(git:*), Bash(gh:*)
argument-hint: [fleet-group] [version]
description: Deploy to production fleet devices
---

## Task

Deploy to production fleet: $1
Version: v$2

Production deployment:
1. Verify release tag exists
2. Run pre-flight checks
3. Deploy to canary devices (10%)
4. Monitor canary health (30 min)
5. Progressive rollout (25%, 50%, 100%)
6. Monitor fleet health
7. Rollback procedure ready

Fleet deployment strategy:
- Group: $1 (test/pilot/production)
- Batch size: 10 devices
- Rollout interval: 15 minutes
- Health check frequency: 5 minutes

Health metrics to monitor:
- GPS fix rate
- Firebase sync success
- Power consumption
- Error rate
- Memory usage
- Network traffic

Rollback triggers:
- Error rate > 5%
- GPS failure > 10%
- Firebase sync failure > 15%
- Device offline > 20%

Post-deployment:
- Update fleet dashboard
- Send deployment report
- Archive release artifacts
- Update documentation
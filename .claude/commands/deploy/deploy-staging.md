---
allowed-tools: Bash(ssh:*), Bash(scp:*), Bash(git:*)
argument-hint: [target-pi] [branch]
description: Deploy to staging Raspberry Pi
---

## Task

Deploy to staging Pi: $1
Branch/Tag: $2

Deployment steps:
1. SSH to target Pi: $1
2. Backup current deployment
3. Pull latest code from $2
4. Install/update dependencies
5. Run database migrations
6. Update configuration
7. Restart services
8. Run health checks
9. Monitor logs for errors

Pre-deployment checks:
- Pi connectivity
- Available disk space
- Battery/power status
- Network configuration
- Firebase credentials

Deployment script:
```bash
# Stop service
sudo systemctl stop fleet-tracker

# Update code
cd /opt/trakscape-fleet
git fetch && git checkout $2
pip install -r requirements.txt

# Update config
cp config/staging.yaml config/config.yaml

# Restart service
sudo systemctl start fleet-tracker
sudo systemctl status fleet-tracker
```

Post-deployment verification:
- GPS data flowing
- Firebase connection active
- UPS monitoring working
- Logs clean
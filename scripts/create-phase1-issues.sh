#!/bin/bash

# Create Phase 1 GitHub Issues for Trakscape Fleet Platform

echo "Creating Phase 1 issues for Trakscape Fleet Platform..."

# Create milestone first
gh api repos/{owner}/{repo}/milestones \
  --method POST \
  -f title="Phase 1 - Core GPS Tracking" \
  -f description="Implement core GPS tracking with cellular connectivity and Firebase integration" \
  -f due_on="2024-03-01T00:00:00Z" \
  2>/dev/null || echo "Milestone might already exist"

# Issue 1: GPS Tracking Module
gh issue create \
  --title "[GPS] Implement GPS tracking module for 4G HAT" \
  --body "$(cat <<EOF
## Overview
Implement GPS tracking module for real-time location data acquisition from 4G HAT.

## Requirements
- Serial port communication with 4G HAT
- AT command interface for GPS control
- NMEA sentence parsing
- Location data validation
- Speed and heading calculation
- GPS fix quality monitoring

## Technical Details
- Serial ports: /dev/ttyUSB0-3
- Baud rate: 115200
- GPS update rate: 1Hz minimum
- Data format: NMEA 0183

## Acceptance Criteria
- GPS module initializes successfully
- Location updates received every 10-30 seconds
- Accurate position within 10 meters
- Handles GPS signal loss gracefully
- Logs GPS events properly

## Dependencies
- pyserial library
- 4G HAT properly configured
- SIM card with data plan
EOF
)" \
  --label "enhancement,phase-1,gps" \
  --milestone "Phase 1 - Core GPS Tracking"

# Issue 2: Firebase Integration
gh issue create \
  --title "[Firebase] Implement Firebase real-time database sync" \
  --body "$(cat <<EOF
## Overview
Implement Firebase integration for real-time GPS data synchronization with offline buffering.

## Requirements
- Firebase project setup
- Authentication configuration
- Real-time database schema
- Offline data buffering
- Batch upload optimization
- Connection state management

## Data Schema
\`\`\`json
{
  "vehicles": {
    "device_id": {
      "current_location": {...},
      "history": {...},
      "status": {...}
    }
  }
}
\`\`\`

## Acceptance Criteria
- Firebase connection established
- Data syncs in real-time when online
- Offline data queued properly
- Batch uploads working
- Data compression reduces bandwidth 50%+

## Dependencies
- firebase-admin SDK
- SQLite for buffering
EOF
)" \
  --label "enhancement,phase-1,firebase,backend" \
  --milestone "Phase 1 - Core GPS Tracking"

# Issue 3: UPS Power Management
gh issue create \
  --title "[UPS] Implement UPS HAT power management" \
  --body "$(cat <<EOF
## Overview
Implement UPS HAT integration for reliable power management and graceful shutdown.

## Requirements
- I2C communication with UPS HAT
- Battery level monitoring
- Power source detection
- Graceful shutdown triggers
- Power event logging
- Battery health tracking

## Technical Details
- I2C address: 0x36
- Communication: SMBus
- Voltage range: 3.0V - 4.2V
- Output: 5V up to 5A

## Acceptance Criteria
- UPS communication established
- Battery level accurate within 5%
- Power loss detected within 1 second
- Graceful shutdown works reliably
- All data saved before shutdown

## Dependencies
- smbus2 library
- RPi.GPIO library
- I2C enabled on Pi
EOF
)" \
  --label "enhancement,phase-1,hardware,power" \
  --milestone "Phase 1 - Core GPS Tracking"

# Issue 4: Data Buffering
gh issue create \
  --title "[Buffer] Implement offline data buffering with SQLite" \
  --body "$(cat <<EOF
## Overview
Implement SQLite-based data buffering for offline operation and sync management.

## Requirements
- SQLite database setup
- Queue management system
- Data compression
- Automatic sync when online
- Data retention policies
- Storage optimization

## Database Schema
\`\`\`sql
CREATE TABLE gps_buffer (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME,
  device_id TEXT,
  latitude REAL,
  longitude REAL,
  speed REAL,
  synced BOOLEAN DEFAULT 0,
  compressed_data BLOB
);
\`\`\`

## Acceptance Criteria
- Database creates successfully
- Data inserts within 10ms
- Compression achieves 60%+ reduction
- Sync resumes after connection
- Old data cleaned automatically

## Dependencies
- sqlite3 (built-in)
- gzip compression
EOF
)" \
  --label "enhancement,phase-1,database,offline" \
  --milestone "Phase 1 - Core GPS Tracking"

# Issue 5: Main Orchestrator
gh issue create \
  --title "[Core] Implement main application orchestrator" \
  --body "$(cat <<EOF
## Overview
Implement main application orchestrator that coordinates all Phase 1 modules.

## Requirements
- Module initialization sequence
- Health monitoring system
- Configuration management
- Error recovery mechanisms
- Logging infrastructure
- Systemd service integration

## Application Structure
\`\`\`python
class FleetTracker:
    - gps_module
    - firebase_sync
    - power_manager
    - data_buffer
    - config_manager
    - health_monitor
\`\`\`

## Acceptance Criteria
- All modules initialize correctly
- Health checks run every 30 seconds
- Failed modules auto-recover
- Configuration hot-reload works
- Service starts on boot

## Dependencies
- PyYAML for config
- asyncio for async ops
- systemd integration
EOF
)" \
  --label "enhancement,phase-1,core,architecture" \
  --milestone "Phase 1 - Core GPS Tracking"

echo "Phase 1 issues created successfully!"
echo "View issues at: https://github.com/$(gh api user -q .login)/trakscape-fleet/issues"
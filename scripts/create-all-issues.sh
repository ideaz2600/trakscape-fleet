#!/bin/bash

echo "Creating comprehensive issue structure for Trakscape Fleet Platform..."

# Create labels first
echo "Creating labels..."
gh label create "epic" --description "High-level phase or major feature" --color "7057FF" 2>/dev/null
gh label create "feature" --description "User-facing functionality" --color "0075CA" 2>/dev/null
gh label create "subtask" --description "Implementation task" --color "008080" 2>/dev/null
gh label create "phase-1" --description "Core Foundation" --color "FF6B6B" 2>/dev/null
gh label create "phase-2" --description "Visual Monitoring" --color "4ECDC4" 2>/dev/null
gh label create "phase-3" --description "Advanced Analytics" --color "45B7D1" 2>/dev/null
gh label create "hardware" --description "Hardware integration" --color "FFA500" 2>/dev/null
gh label create "gps" --description "GPS tracking" --color "2ECC71" 2>/dev/null
gh label create "cellular" --description "4G/LTE connectivity" --color "3498DB" 2>/dev/null
gh label create "power" --description "Power management" --color "E74C3C" 2>/dev/null
gh label create "firebase" --description "Cloud backend" --color "F39C12" 2>/dev/null
gh label create "camera" --description "Camera system" --color "9B59B6" 2>/dev/null
gh label create "imu" --description "IMU sensor" --color "1ABC9C" 2>/dev/null
gh label create "canbus" --description "CAN bus interface" --color "34495E" 2>/dev/null
gh label create "nfc" --description "NFC identification" --color "E91E63" 2>/dev/null

# Create milestones
echo "Creating milestones..."
gh api repos/{owner}/{repo}/milestones \
  --method POST \
  -f title="Phase 1: Core Foundation" \
  -f description="GPS + Cellular + Basic Logging + Firebase + Power Management" \
  -f due_on="2024-02-01T00:00:00Z" 2>/dev/null

gh api repos/{owner}/{repo}/milestones \
  --method POST \
  -f title="Phase 2: Visual Monitoring" \
  -f description="Camera modules + Night vision + Image processing" \
  -f due_on="2024-03-01T00:00:00Z" 2>/dev/null

gh api repos/{owner}/{repo}/milestones \
  --method POST \
  -f title="Phase 3: Advanced Analytics" \
  -f description="IMU + CAN bus + NFC identification" \
  -f due_on="2024-04-01T00:00:00Z" 2>/dev/null

# ====================
# PHASE 1: CORE FOUNDATION
# ====================

echo "Creating Phase 1 Epic and features..."

# Phase 1 Epic
EPIC1=$(gh issue create \
  --title "[EPIC] Phase 1: Core Foundation - GPS & Cellular MVP" \
  --body "$(cat <<EOF
## Epic Overview
Implement the core foundation of the fleet tracking system with GPS tracking, cellular connectivity, Firebase integration, and reliable power management.

## Business Value
- Enable real-time vehicle location tracking
- Establish reliable data pipeline to cloud
- Ensure system reliability with power management
- Create foundation for future features

## Success Criteria
- [ ] Continuous GPS tracking with 10-30 second updates
- [ ] Reliable 4G/LTE data transmission
- [ ] Firebase real-time database integration
- [ ] 7-day offline data buffering
- [ ] Graceful shutdown on power loss
- [ ] System auto-starts on boot
- [ ] 95% uptime achieved

## Features
- [ ] Raspberry Pi 5 Setup with NVMe Storage
- [ ] 4G HAT Cellular Connectivity
- [ ] GPS Location Tracking
- [ ] Firebase Cloud Pipeline
- [ ] UPS Power Management
- [ ] System Service & Monitoring

## Dependencies
- Hardware components available
- SIM card with data plan
- Firebase project created
- Development environment setup

## Timeline
- Start Date: January 2024
- Target Completion: February 2024

## Risks & Mitigation
- GPS signal loss in urban canyons → Implement dead reckoning
- Cellular coverage gaps → Robust offline buffering
- Power interruptions → UPS with graceful shutdown
- Data costs → Compression and batch uploads
EOF
)" \
  --label "epic,phase-1" \
  --milestone "Phase 1: Core Foundation" \
  --json number -q .number)

echo "Created Phase 1 Epic: #$EPIC1"

# Feature 1: Raspberry Pi Setup
FEATURE1=$(gh issue create \
  --title "[FEATURE] Raspberry Pi 5 Setup with NVMe Storage" \
  --body "$(cat <<EOF
## Feature Description
Set up Raspberry Pi 5 with NVMe SSD for reliable storage and optimal performance.

## User Story
As a fleet manager
I want a reliable hardware platform
So that the tracking system operates continuously without storage failures

## Acceptance Criteria
- [ ] Raspberry Pi 5 boots from NVMe SSD
- [ ] 256GB storage properly partitioned
- [ ] OS configured and optimized
- [ ] All required interfaces enabled (I2C, SPI, Serial, GPIO)
- [ ] Python 3.9+ installed with virtual environment
- [ ] Development tools installed

## Technical Requirements
- Raspberry Pi OS Lite (64-bit)
- NVMe boot configuration
- Swap file configuration
- Temperature monitoring
- Overclock settings (optional)

## Subtasks
- [ ] Flash and configure Raspberry Pi OS
- [ ] Enable hardware interfaces
- [ ] Install Python and dependencies
- [ ] Configure networking
- [ ] Set up remote access

## Parent Epic
Related to #$EPIC1
EOF
)" \
  --label "feature,phase-1,hardware" \
  --milestone "Phase 1: Core Foundation" \
  --json number -q .number)

# Feature 2: 4G HAT Setup
FEATURE2=$(gh issue create \
  --title "[FEATURE] 4G HAT Cellular Connectivity" \
  --body "$(cat <<EOF
## Feature Description
Configure 4G/LTE HAT for reliable cellular data connectivity and GPS functionality.

## User Story
As a fleet operator
I want continuous cellular connectivity
So that vehicle data is transmitted in real-time

## Acceptance Criteria
- [ ] 4G HAT recognized by system
- [ ] Cellular connection auto-establishes
- [ ] Connection monitoring and auto-recovery
- [ ] Data usage optimization implemented
- [ ] GPS module accessible via serial
- [ ] Network failover handling

## Technical Requirements
- AT command interface
- PPP connection setup
- QMI/MBIM protocol support
- Serial port configuration
- Network manager integration

## Subtasks
- [ ] Install 4G HAT drivers and tools
- [ ] Configure serial ports
- [ ] Set up PPP connection
- [ ] Implement connection monitoring
- [ ] Create data usage tracking

## Parent Epic
Related to #$EPIC1
EOF
)" \
  --label "feature,phase-1,cellular,hardware" \
  --milestone "Phase 1: Core Foundation" \
  --json number -q .number)

# Feature 3: GPS Tracking
FEATURE3=$(gh issue create \
  --title "[FEATURE] GPS Location Tracking System" \
  --body "$(cat <<EOF
## Feature Description
Implement GPS tracking to capture vehicle location, speed, and heading data.

## User Story
As a fleet manager
I want accurate vehicle location data
So that I can monitor fleet movements in real-time

## Acceptance Criteria
- [ ] GPS module initialized via AT commands
- [ ] Location updates every 10-30 seconds
- [ ] Accuracy within 10 meters
- [ ] Speed and heading calculated
- [ ] GPS signal quality monitoring
- [ ] Handle signal loss gracefully

## Technical Requirements
- NMEA sentence parsing
- Coordinate system conversion
- Speed/heading calculation
- Geofencing capability
- Time synchronization

## Subtasks
- [ ] Implement GPS AT command interface
- [ ] Create NMEA parser
- [ ] Build location data model
- [ ] Add data validation
- [ ] Implement error recovery

## Parent Epic
Related to #$EPIC1
EOF
)" \
  --label "feature,phase-1,gps" \
  --milestone "Phase 1: Core Foundation" \
  --json number -q .number)

# Feature 4: Firebase Integration
FEATURE4=$(gh issue create \
  --title "[FEATURE] Firebase Cloud Data Pipeline" \
  --body "$(cat <<EOF
## Feature Description
Establish Firebase real-time database connection for cloud data storage and sync.

## User Story
As a fleet manager
I want vehicle data stored in the cloud
So that I can access it from anywhere via web/mobile apps

## Acceptance Criteria
- [ ] Firebase project configured
- [ ] Service account authentication working
- [ ] Real-time database schema defined
- [ ] Data compression before upload
- [ ] Batch upload optimization
- [ ] Offline queue management

## Technical Requirements
- Firebase Admin SDK
- Data compression (gzip)
- Batch processing
- Connection state management
- Retry logic
- Rate limiting

## Subtasks
- [ ] Set up Firebase project
- [ ] Design database schema
- [ ] Implement authentication
- [ ] Create sync manager
- [ ] Build offline queue
- [ ] Add compression layer

## Parent Epic
Related to #$EPIC1
EOF
)" \
  --label "feature,phase-1,firebase" \
  --milestone "Phase 1: Core Foundation" \
  --json number -q .number)

# Feature 5: UPS Power Management
FEATURE5=$(gh issue create \
  --title "[FEATURE] UPS Power Management System" \
  --body "$(cat <<EOF
## Feature Description
Integrate UPS HAT for reliable power management and graceful shutdown capabilities.

## User Story
As a fleet operator
I want the system to handle power interruptions
So that no data is lost during vehicle shutdown

## Acceptance Criteria
- [ ] UPS HAT communication established
- [ ] Battery level monitoring accurate
- [ ] Power loss detected within 1 second
- [ ] Graceful shutdown process works
- [ ] Data saved before shutdown
- [ ] Auto-recovery on power restore

## Technical Requirements
- I2C communication protocol
- Battery voltage monitoring
- Current draw measurement
- Temperature monitoring
- Shutdown sequencing

## Subtasks
- [ ] Configure I2C interface
- [ ] Implement battery monitoring
- [ ] Create power event handlers
- [ ] Build shutdown sequence
- [ ] Add recovery logic

## Parent Epic
Related to #$EPIC1
EOF
)" \
  --label "feature,phase-1,power,hardware" \
  --milestone "Phase 1: Core Foundation" \
  --json number -q .number)

# Now create subtasks for each feature
echo "Creating Phase 1 subtasks..."

# Subtasks for Feature 1 (Pi Setup)
gh issue create \
  --title "[SUBTASK] Flash and configure Raspberry Pi OS on NVMe" \
  --body "Flash Raspberry Pi OS Lite 64-bit to NVMe SSD, configure boot partition, and set up initial system configuration. Related to #$FEATURE1" \
  --label "subtask,phase-1,hardware"

gh issue create \
  --title "[SUBTASK] Enable I2C, SPI, Serial, and GPIO interfaces" \
  --body "Enable all required hardware interfaces via raspi-config for HAT communication. Related to #$FEATURE1" \
  --label "subtask,phase-1,hardware"

# Subtasks for Feature 2 (4G HAT)
gh issue create \
  --title "[SUBTASK] Install and configure 4G HAT drivers" \
  --body "Install Simcom drivers, configure ModemManager, and set up PPP connection scripts. Related to #$FEATURE2" \
  --label "subtask,phase-1,cellular"

gh issue create \
  --title "[SUBTASK] Implement cellular connection monitoring" \
  --body "Create service to monitor connection status, handle reconnections, and track data usage. Related to #$FEATURE2" \
  --label "subtask,phase-1,cellular"

# Subtasks for Feature 3 (GPS)
gh issue create \
  --title "[SUBTASK] Implement GPS AT command interface" \
  --body "Create Python module to send AT commands for GPS control (AT+CGPS=1, AT+CGPSINFO). Related to #$FEATURE3" \
  --label "subtask,phase-1,gps"

gh issue create \
  --title "[SUBTASK] Build NMEA sentence parser" \
  --body "Parse GPRMC, GPGGA sentences for location, speed, heading extraction. Related to #$FEATURE3" \
  --label "subtask,phase-1,gps"

# Subtasks for Feature 4 (Firebase)
gh issue create \
  --title "[SUBTASK] Design Firebase database schema" \
  --body "Create schema for vehicles, locations, history, and status data. Related to #$FEATURE4" \
  --label "subtask,phase-1,firebase"

gh issue create \
  --title "[SUBTASK] Implement offline data buffering with SQLite" \
  --body "Create SQLite database for offline queue with compression and batch processing. Related to #$FEATURE4" \
  --label "subtask,phase-1,firebase"

# Subtasks for Feature 5 (UPS)
gh issue create \
  --title "[SUBTASK] Configure I2C communication with UPS HAT" \
  --body "Set up SMBus communication to read battery voltage, current, and status. Related to #$FEATURE5" \
  --label "subtask,phase-1,power"

gh issue create \
  --title "[SUBTASK] Implement graceful shutdown sequence" \
  --body "Create shutdown handler that saves data, closes connections, and powers down safely. Related to #$FEATURE5" \
  --label "subtask,phase-1,power"

# ====================
# PHASE 2: VISUAL MONITORING
# ====================

echo "Creating Phase 2 Epic and features..."

# Phase 2 Epic
EPIC2=$(gh issue create \
  --title "[EPIC] Phase 2: Visual Monitoring - Camera System" \
  --body "$(cat <<EOF
## Epic Overview
Add visual monitoring capabilities with multiple camera modules, night vision, and intelligent image capture/processing.

## Business Value
- Visual verification of events
- Driver behavior monitoring
- Evidence for incidents
- Enhanced security

## Success Criteria
- [ ] Multi-camera system operational
- [ ] Night vision working
- [ ] Event-triggered capture
- [ ] Efficient image compression
- [ ] Selective cloud upload

## Features
- [ ] Forward-facing camera
- [ ] Driver-facing camera
- [ ] Night vision capability
- [ ] Image processing pipeline
- [ ] Selective upload strategy

## Dependencies
- Phase 1 completed
- Sufficient processing power
- Storage for images
- Bandwidth for uploads

## Timeline
- Start Date: February 2024
- Target Completion: March 2024
EOF
)" \
  --label "epic,phase-2" \
  --milestone "Phase 2: Visual Monitoring" \
  --json number -q .number)

# Phase 2 Features
gh issue create \
  --title "[FEATURE] Forward-Facing Camera System" \
  --body "Implement forward-facing camera for road/traffic monitoring with event-triggered capture. Related to #$EPIC2" \
  --label "feature,phase-2,camera" \
  --milestone "Phase 2: Visual Monitoring"

gh issue create \
  --title "[FEATURE] Driver-Facing Camera with IR" \
  --body "Set up driver monitoring camera with infrared LEDs for day/night operation. Related to #$EPIC2" \
  --label "feature,phase-2,camera" \
  --milestone "Phase 2: Visual Monitoring"

gh issue create \
  --title "[FEATURE] Image Processing Pipeline" \
  --body "Create pipeline for image capture, compression, analysis, and selective storage. Related to #$EPIC2" \
  --label "feature,phase-2,camera" \
  --milestone "Phase 2: Visual Monitoring"

# ====================
# PHASE 3: ADVANCED ANALYTICS
# ====================

echo "Creating Phase 3 Epic and features..."

# Phase 3 Epic
EPIC3=$(gh issue create \
  --title "[EPIC] Phase 3: Advanced Analytics - IMU, CAN, NFC" \
  --body "$(cat <<EOF
## Epic Overview
Implement advanced analytics with IMU for driving behavior, CAN bus for vehicle diagnostics, and NFC for driver identification.

## Business Value
- Driving behavior analysis
- Vehicle health monitoring
- Driver identification and hours tracking
- Predictive maintenance

## Success Criteria
- [ ] IMU capturing acceleration/rotation data
- [ ] CAN bus reading vehicle diagnostics
- [ ] NFC identifying drivers
- [ ] Analytics dashboard operational
- [ ] Alerts for aggressive driving

## Features
- [ ] BNO055 IMU integration
- [ ] CAN bus monitoring
- [ ] NFC driver identification
- [ ] Behavior analytics engine
- [ ] Diagnostic reporting

## Dependencies
- Phases 1 & 2 completed
- CAN interface in vehicle
- NFC cards for drivers
- Analytics backend

## Timeline
- Start Date: March 2024
- Target Completion: April 2024
EOF
)" \
  --label "epic,phase-3" \
  --milestone "Phase 3: Advanced Analytics" \
  --json number -q .number)

# Phase 3 Features
gh issue create \
  --title "[FEATURE] BNO055 IMU Integration" \
  --body "Integrate 9-DOF IMU for acceleration, rotation, and orientation tracking. Related to #$EPIC3" \
  --label "feature,phase-3,imu" \
  --milestone "Phase 3: Advanced Analytics"

gh issue create \
  --title "[FEATURE] CAN Bus Vehicle Diagnostics" \
  --body "Implement CAN FD interface for reading vehicle speed, RPM, fuel, temperature. Related to #$EPIC3" \
  --label "feature,phase-3,canbus" \
  --milestone "Phase 3: Advanced Analytics"

gh issue create \
  --title "[FEATURE] NFC Driver Identification" \
  --body "Set up NFC reader for driver check-in/out and hours tracking. Related to #$EPIC3" \
  --label "feature,phase-3,nfc" \
  --milestone "Phase 3: Advanced Analytics"

echo "All issues created successfully!"
echo "View issues at: https://github.com/ideaz2600/trakscape-fleet/issues"
echo ""
echo "Summary:"
echo "- 3 Epics (Phase 1, 2, 3)"
echo "- 13+ Features across all phases"
echo "- 10+ Subtasks for Phase 1 implementation"
echo "- Labels and milestones configured"
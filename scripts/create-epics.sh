#!/bin/bash

echo "Creating Epic issues..."

# Phase 1 Epic
gh issue create \
  --title "[EPIC] Phase 1: Core Foundation - GPS & Cellular MVP" \
  --body "## Epic Overview
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
- [ ] #17 Raspberry Pi 5 Setup with NVMe Storage
- [ ] #18 4G HAT Cellular Connectivity
- [ ] #19 GPS Location Tracking
- [ ] #20 Firebase Cloud Pipeline
- [ ] #21 UPS Power Management
- [ ] System Service & Monitoring

## Dependencies
- Hardware components available
- SIM card with data plan
- Firebase project created
- Development environment setup

## Timeline
- Start Date: January 2024
- Target Completion: February 2024" \
  --label "epic,phase-1" \
  --milestone "Phase 1: Core Foundation"

# Phase 2 Epic
gh issue create \
  --title "[EPIC] Phase 2: Visual Monitoring - Camera System" \
  --body "## Epic Overview
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
- [ ] #11 Forward-facing camera
- [ ] #12 Driver-facing camera
- [ ] Night vision capability
- [ ] #13 Image processing pipeline
- [ ] Selective upload strategy

## Dependencies
- Phase 1 completed
- Sufficient processing power
- Storage for images
- Bandwidth for uploads

## Timeline
- Start Date: February 2024
- Target Completion: March 2024" \
  --label "epic,phase-2" \
  --milestone "Phase 2: Visual Monitoring"

# Phase 3 Epic
gh issue create \
  --title "[EPIC] Phase 3: Advanced Analytics - IMU, CAN, NFC" \
  --body "## Epic Overview
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
- [ ] #14 BNO055 IMU integration
- [ ] #15 CAN bus monitoring
- [ ] #16 NFC driver identification
- [ ] Behavior analytics engine
- [ ] Diagnostic reporting

## Dependencies
- Phases 1 & 2 completed
- CAN interface in vehicle
- NFC cards for drivers
- Analytics backend

## Timeline
- Start Date: March 2024
- Target Completion: April 2024" \
  --label "epic,phase-3" \
  --milestone "Phase 3: Advanced Analytics"

# Create missing Phase 1 features
echo "Creating missing Phase 1 features..."

gh issue create \
  --title "[FEATURE] Raspberry Pi 5 Setup with NVMe Storage" \
  --body "## Feature Description
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

## Subtasks
- [ ] #1 Flash and configure Raspberry Pi OS
- [ ] #2 Enable hardware interfaces
- [ ] Install Python and dependencies
- [ ] Configure networking
- [ ] Set up remote access" \
  --label "feature,phase-1,hardware" \
  --milestone "Phase 1: Core Foundation"

gh issue create \
  --title "[FEATURE] 4G HAT Cellular Connectivity" \
  --body "## Feature Description
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

## Subtasks
- [ ] #3 Install 4G HAT drivers and tools
- [ ] Configure serial ports
- [ ] Set up PPP connection
- [ ] #4 Implement connection monitoring
- [ ] Create data usage tracking" \
  --label "feature,phase-1,cellular,hardware" \
  --milestone "Phase 1: Core Foundation"

gh issue create \
  --title "[FEATURE] GPS Location Tracking System" \
  --body "## Feature Description
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

## Subtasks
- [ ] #5 Implement GPS AT command interface
- [ ] #6 Create NMEA parser
- [ ] Build location data model
- [ ] Add data validation
- [ ] Implement error recovery" \
  --label "feature,phase-1,gps" \
  --milestone "Phase 1: Core Foundation"

gh issue create \
  --title "[FEATURE] Firebase Cloud Data Pipeline" \
  --body "## Feature Description
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

## Subtasks
- [ ] Set up Firebase project
- [ ] #7 Design database schema
- [ ] Implement authentication
- [ ] Create sync manager
- [ ] #8 Build offline queue
- [ ] Add compression layer" \
  --label "feature,phase-1,firebase" \
  --milestone "Phase 1: Core Foundation"

gh issue create \
  --title "[FEATURE] UPS Power Management System" \
  --body "## Feature Description
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

## Subtasks
- [ ] #9 Configure I2C interface
- [ ] Implement battery monitoring
- [ ] Create power event handlers
- [ ] #10 Build shutdown sequence
- [ ] Add recovery logic" \
  --label "feature,phase-1,power,hardware" \
  --milestone "Phase 1: Core Foundation"

echo "All epics and features created!"
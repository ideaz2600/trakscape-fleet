---
allowed-tools: Bash(python:*), Bash(pytest:*), Bash(git:*)
argument-hint: [feature-name] [test-type]
description: Run comprehensive tests for a feature
---

## Task

Test feature: $1
Test type: $2 (unit/integration/hardware/all)

Test execution:
1. Unit tests for $1 module
2. Integration tests with dependencies
3. Hardware tests on Pi (if applicable)
4. Performance benchmarks
5. Memory profiling
6. Network failure simulations

Phase 1 specific tests:

**GPS Module:**
- Serial communication
- NMEA parsing
- Signal loss handling
- Location accuracy

**Firebase Sync:**
- Connection establishment
- Data compression
- Batch uploads
- Offline queue
- Retry logic

**UPS Management:**
- Battery level reading
- Shutdown triggers
- Power event detection
- Failover testing

**Data Buffer:**
- SQLite operations
- Queue management
- Data persistence
- Cleanup routines

Generate coverage report and identify gaps.
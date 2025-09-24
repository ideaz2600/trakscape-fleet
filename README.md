# Trakscape Fleet Platform

Real-time GPS fleet tracking system for Raspberry Pi devices with cellular connectivity and cloud integration.

## Phase 1: Core GPS Tracking System

### Hardware Components
- Raspberry Pi 5 (8GB) with NVMe SSD
- 4G/3G/2G/GSM/GPRS/GNSS HAT (LTE CAT4)
- UPS HAT for power management
- Camera modules (Phase 2)
- IMU sensor (Phase 3)
- CAN bus interface (Phase 3)

### Features
- Real-time GPS tracking via cellular network
- Firebase cloud integration
- Offline data buffering with automatic sync
- Power management with graceful shutdown
- Configurable update intervals
- Data compression for bandwidth optimization

## Quick Start

### Prerequisites
- Raspberry Pi 5 running Raspberry Pi OS
- Python 3.9+
- Active SIM card with data plan
- Firebase project with credentials

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/trakscape-fleet.git
cd trakscape-fleet

# Install dependencies
pip install -r requirements.txt

# Configure hardware
sudo raspi-config
# Enable: I2C, SPI, Serial

# Set up configuration
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your settings

# Install as service
sudo ./install.sh
```

## Project Structure

```
trakscape-fleet/
├── src/              # Source code
├── config/           # Configuration files
├── tests/            # Test suite
├── docs/             # Documentation
├── systemd/          # Service files
└── .claude/          # Development commands
```

## Development

Use Claude commands for workflow management:
- `/start-feature [issue-number]` - Start new feature
- `/list-issues` - View open issues
- `/project-status` - Get project overview

## License

Proprietary - Trakscape Fleet Platform
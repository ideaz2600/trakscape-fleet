#!/bin/bash

# Trakscape Fleet Platform Installation Script

set -e

echo "==================================="
echo "Trakscape Fleet Platform Installer"
echo "==================================="

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    i2c-tools \
    minicom \
    sqlite3 \
    ppp \
    usb-modeswitch \
    usb-modeswitch-data

# Enable hardware interfaces
echo "Enabling hardware interfaces..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_serial 0

# Install Python dependencies
echo "Installing Python dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
echo "Creating directories..."
mkdir -p data logs config

# Copy configuration
if [ ! -f config/config.yaml ]; then
    echo "Creating configuration file..."
    cp config/config.example.yaml config/config.yaml
    echo "Please edit config/config.yaml with your settings"
fi

# Install systemd service
echo "Installing systemd service..."
sudo cp systemd/fleet-tracker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fleet-tracker.service

# Setup 4G HAT
echo "Setting up 4G HAT..."
# Add udev rules for 4G HAT
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="1e0e", ATTRS{idProduct}=="9001", SYMLINK+="gps"' | sudo tee /etc/udev/rules.d/99-gps.rules
sudo udevadm control --reload-rules

echo "================================"
echo "Installation complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit config/config.yaml with your Firebase credentials and device settings"
echo "2. Add your Firebase service account key to config/firebase_key.json"
echo "3. Configure your cellular APN in config/config.yaml"
echo "4. Start the service: sudo systemctl start fleet-tracker"
echo "5. Check logs: sudo journalctl -u fleet-tracker -f"
echo ""
echo "To start the service on boot:"
echo "sudo systemctl enable fleet-tracker"
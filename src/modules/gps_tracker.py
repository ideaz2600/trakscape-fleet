"""GPS tracking module for 4G HAT"""

import serial
import time
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
import re
from threading import Thread, Event


class GPSTracker:
    """Handles GPS tracking via 4G HAT serial interface"""

    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.stop_event = Event()
        self.last_position = None

    def connect(self) -> bool:
        """Establish serial connection to GPS module"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1,
                write_timeout=1
            )
            self.logger.info(f"Connected to GPS on {self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to GPS: {e}")
            return False

    def send_at_command(self, command: str) -> str:
        """Send AT command and get response"""
        if not self.serial:
            return ""

        try:
            self.serial.write(f"{command}\r\n".encode())
            time.sleep(0.1)
            response = self.serial.read(self.serial.in_waiting).decode()
            return response
        except Exception as e:
            self.logger.error(f"AT command error: {e}")
            return ""

    def enable_gps(self) -> bool:
        """Enable GPS module via AT commands"""
        response = self.send_at_command("AT+CGPS=1,1")
        if "OK" in response:
            self.logger.info("GPS enabled successfully")
            return True
        else:
            self.logger.error(f"Failed to enable GPS: {response}")
            return False

    def get_gps_info(self) -> Optional[Dict]:
        """Get current GPS information"""
        response = self.send_at_command("AT+CGPSINFO")

        # Parse response: +CGPSINFO: lat,N,lon,E,date,time,alt,speed,course
        pattern = r'\+CGPSINFO:\s*([0-9.]+),([NS]),([0-9.]+),([EW])'
        match = re.search(pattern, response)

        if match:
            lat_str, lat_dir, lon_str, lon_dir = match.groups()

            # Convert to decimal degrees
            lat = self._convert_to_decimal(lat_str, lat_dir)
            lon = self._convert_to_decimal(lon_str, lon_dir)

            return {
                'latitude': lat,
                'longitude': lon,
                'timestamp': datetime.utcnow().isoformat(),
                'valid': True
            }

        return None

    def _convert_to_decimal(self, coord_str: str, direction: str) -> float:
        """Convert GPS coordinates to decimal degrees"""
        # Format: DDMM.MMMM
        if len(coord_str) < 4:
            return 0.0

        # Extract degrees and minutes
        if len(coord_str) > 10:  # Longitude
            degrees = float(coord_str[:3])
            minutes = float(coord_str[3:])
        else:  # Latitude
            degrees = float(coord_str[:2])
            minutes = float(coord_str[2:])

        decimal = degrees + (minutes / 60.0)

        # Apply direction
        if direction in ['S', 'W']:
            decimal = -decimal

        return decimal

    def parse_nmea(self, sentence: str) -> Optional[Dict]:
        """Parse NMEA sentence for GPS data"""
        if not sentence.startswith('$'):
            return None

        parts = sentence.split(',')

        # Parse GPRMC sentence (Recommended Minimum)
        if parts[0] == '$GPRMC' and len(parts) >= 12:
            if parts[2] == 'A':  # A=Active, V=Void
                lat = self._parse_coordinate(parts[3], parts[4])
                lon = self._parse_coordinate(parts[5], parts[6])
                speed_knots = float(parts[7]) if parts[7] else 0
                speed_kmh = speed_knots * 1.852
                heading = float(parts[8]) if parts[8] else 0

                return {
                    'latitude': lat,
                    'longitude': lon,
                    'speed': speed_kmh,
                    'heading': heading,
                    'timestamp': datetime.utcnow().isoformat(),
                    'valid': True
                }

        return None

    def _parse_coordinate(self, value: str, direction: str) -> float:
        """Parse NMEA coordinate format"""
        if not value:
            return 0.0

        # DDMM.MMMM format
        if len(value) > 10:  # Longitude
            degrees = float(value[:3])
            minutes = float(value[3:])
        else:  # Latitude
            degrees = float(value[:2])
            minutes = float(value[2:])

        decimal = degrees + (minutes / 60.0)

        if direction in ['S', 'W']:
            decimal = -decimal

        return decimal

    def start_tracking(self, callback=None):
        """Start continuous GPS tracking"""
        if not self.serial:
            self.connect()

        if not self.enable_gps():
            return False

        self.running = True
        self.stop_event.clear()

        def track():
            while self.running and not self.stop_event.is_set():
                position = self.get_gps_info()
                if position:
                    self.last_position = position
                    if callback:
                        callback(position)
                    self.logger.debug(f"GPS: {position}")

                self.stop_event.wait(10)  # Update interval

        Thread(target=track, daemon=True).start()
        return True

    def stop_tracking(self):
        """Stop GPS tracking"""
        self.running = False
        self.stop_event.set()
        self.send_at_command("AT+CGPS=0")

    def close(self):
        """Close serial connection"""
        if self.serial:
            self.serial.close()
            self.serial = None
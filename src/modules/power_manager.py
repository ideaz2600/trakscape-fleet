"""UPS HAT power management module"""

import logging
import time
from typing import Dict, Optional, Callable
from threading import Thread, Event
import smbus2
import subprocess
import os


class PowerManager:
    """Manages UPS HAT for power monitoring and graceful shutdown"""

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.i2c_address = config.get('i2c_address', 0x36)
        self.bus = None
        self.monitoring = False
        self.stop_event = Event()
        self.shutdown_callback = None
        self.last_status = {}

    def initialize(self) -> bool:
        """Initialize I2C communication with UPS HAT"""
        try:
            self.bus = smbus2.SMBus(1)  # I2C bus 1
            # Test communication
            self.bus.read_byte(self.i2c_address)
            self.logger.info(f"UPS HAT initialized at address 0x{self.i2c_address:02X}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize UPS HAT: {e}")
            return False

    def read_voltage(self) -> float:
        """Read battery voltage"""
        try:
            # Read voltage registers (example for common UPS HAT)
            voltage_raw = self.bus.read_word_data(self.i2c_address, 0x02)
            # Convert to actual voltage (scale factor depends on HAT)
            voltage = (voltage_raw & 0xFFFF) * 0.00125  # Example scaling
            return voltage
        except Exception as e:
            self.logger.error(f"Failed to read voltage: {e}")
            return 0.0

    def read_current(self) -> float:
        """Read current draw"""
        try:
            current_raw = self.bus.read_word_data(self.i2c_address, 0x04)
            # Convert to actual current (mA)
            current = (current_raw & 0xFFFF) * 0.1  # Example scaling
            return current
        except Exception as e:
            self.logger.error(f"Failed to read current: {e}")
            return 0.0

    def read_capacity(self) -> int:
        """Read battery capacity percentage"""
        try:
            capacity = self.bus.read_byte_data(self.i2c_address, 0x0D)
            return min(100, max(0, capacity))
        except Exception as e:
            self.logger.error(f"Failed to read capacity: {e}")
            return 0

    def is_charging(self) -> bool:
        """Check if battery is charging"""
        try:
            status = self.bus.read_byte_data(self.i2c_address, 0x01)
            return (status & 0x01) != 0  # Bit 0 indicates charging
        except Exception as e:
            self.logger.error(f"Failed to read charging status: {e}")
            return False

    def is_external_power(self) -> bool:
        """Check if external power is connected"""
        try:
            status = self.bus.read_byte_data(self.i2c_address, 0x01)
            return (status & 0x02) != 0  # Bit 1 indicates external power
        except Exception as e:
            self.logger.error(f"Failed to read power status: {e}")
            return False

    def get_status(self) -> Dict:
        """Get complete power status"""
        status = {
            'voltage': self.read_voltage(),
            'current': self.read_current(),
            'capacity': self.read_capacity(),
            'charging': self.is_charging(),
            'external_power': self.is_external_power(),
            'timestamp': time.time()
        }
        self.last_status = status
        return status

    def monitor_power(self):
        """Monitor power status and trigger events"""
        check_interval = self.config.get('check_interval', 10)
        low_threshold = self.config.get('low_battery_threshold', 20)
        critical_threshold = self.config.get('critical_battery_threshold', 5)
        shutdown_delay = self.config.get('shutdown_delay', 60)

        power_lost_time = None
        low_battery_warned = False
        critical_battery_warned = False

        while self.monitoring and not self.stop_event.is_set():
            try:
                status = self.get_status()

                # Check external power loss
                if not status['external_power'] and status.get('voltage', 0) > 0:
                    if power_lost_time is None:
                        power_lost_time = time.time()
                        self.logger.warning("External power lost!")
                        self.trigger_event('POWER_LOST', status)
                else:
                    if power_lost_time is not None:
                        self.logger.info("External power restored")
                        self.trigger_event('POWER_RESTORED', status)
                        power_lost_time = None
                        low_battery_warned = False
                        critical_battery_warned = False

                # Check battery levels
                capacity = status['capacity']

                if capacity <= critical_threshold and not critical_battery_warned:
                    self.logger.critical(f"Battery critical: {capacity}%")
                    self.trigger_event('BATTERY_CRITICAL', status)
                    critical_battery_warned = True

                    # Initiate shutdown if on battery power
                    if not status['external_power']:
                        self.initiate_shutdown(shutdown_delay)

                elif capacity <= low_threshold and not low_battery_warned:
                    self.logger.warning(f"Battery low: {capacity}%")
                    self.trigger_event('BATTERY_LOW', status)
                    low_battery_warned = True

                # Reset warnings if battery is charging
                if status['charging'] and capacity > low_threshold:
                    low_battery_warned = False
                    critical_battery_warned = False

                # Log status periodically
                self.logger.debug(f"Power status: {status}")

            except Exception as e:
                self.logger.error(f"Power monitoring error: {e}")

            self.stop_event.wait(check_interval)

    def trigger_event(self, event_type: str, status: Dict):
        """Trigger power event callbacks"""
        self.logger.info(f"Power event: {event_type}")
        # Could implement event callbacks here
        pass

    def initiate_shutdown(self, delay: int):
        """Initiate graceful shutdown"""
        self.logger.critical(f"Initiating shutdown in {delay} seconds")
        self.trigger_event('SHUTDOWN_INITIATED', self.last_status)

        def shutdown_sequence():
            time.sleep(delay)

            # Call shutdown callback if registered
            if self.shutdown_callback:
                try:
                    self.shutdown_callback()
                except Exception as e:
                    self.logger.error(f"Shutdown callback error: {e}")

            # System shutdown
            self.logger.critical("Executing system shutdown")
            try:
                subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            except Exception as e:
                self.logger.error(f"Shutdown command failed: {e}")

        Thread(target=shutdown_sequence, daemon=False).start()

    def start(self, shutdown_callback: Optional[Callable] = None):
        """Start power monitoring"""
        if not self.bus:
            if not self.initialize():
                return False

        self.shutdown_callback = shutdown_callback
        self.monitoring = True
        self.stop_event.clear()
        Thread(target=self.monitor_power, daemon=True).start()
        self.logger.info("Power monitoring started")
        return True

    def stop(self):
        """Stop power monitoring"""
        self.monitoring = False
        self.stop_event.set()
        if self.bus:
            self.bus.close()
        self.logger.info("Power monitoring stopped")
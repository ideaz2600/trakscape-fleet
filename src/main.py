#!/usr/bin/env python3
"""Main application for Trakscape Fleet Platform"""

import os
import sys
import signal
import time
import logging
import logging.handlers
from typing import Optional
from threading import Event

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config_manager import ConfigManager
from modules.gps_tracker import GPSTracker
from modules.firebase_sync import FirebaseSync
from modules.power_manager import PowerManager
from modules.data_buffer import DataBuffer


class FleetTracker:
    """Main Fleet Tracking Application"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
        self.logger = self.setup_logging()
        self.running = False
        self.stop_event = Event()

        # Module instances
        self.gps_tracker = None
        self.firebase_sync = None
        self.power_manager = None
        self.data_buffer = None

    def setup_logging(self) -> logging.Logger:
        """Setup application logging"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_file = log_config.get('file', 'logs/fleet_tracker.log')

        # Create logs directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Setup logger
        logger = logging.getLogger('fleet_tracker')
        logger.setLevel(log_level)

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(console)

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=log_config.get('max_size_mb', 100) * 1024 * 1024,
            backupCount=log_config.get('backup_count', 5)
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

        return logger

    def initialize_modules(self) -> bool:
        """Initialize all modules"""
        self.logger.info("Initializing Fleet Tracker modules...")

        # Initialize data buffer
        self.logger.info("Initializing data buffer...")
        self.data_buffer = DataBuffer(self.config.get('buffer', {}))
        if not self.data_buffer.initialize():
            self.logger.error("Failed to initialize data buffer")
            return False

        # Initialize GPS tracker
        self.logger.info("Initializing GPS tracker...")
        gps_config = self.config.get('gps', {})
        self.gps_tracker = GPSTracker(
            port=gps_config.get('port', '/dev/ttyUSB2'),
            baudrate=gps_config.get('baudrate', 115200)
        )
        if not self.gps_tracker.connect():
            self.logger.warning("GPS tracker not available")

        # Initialize Firebase sync
        self.logger.info("Initializing Firebase sync...")
        firebase_config = self.config.get('firebase', {})
        firebase_config['device_id'] = self.config.get('device', {}).get('id', 'unknown')
        self.firebase_sync = FirebaseSync(firebase_config)
        if not self.firebase_sync.initialize():
            self.logger.warning("Firebase sync not available")

        # Initialize power manager
        self.logger.info("Initializing power manager...")
        self.power_manager = PowerManager(self.config.get('power', {}))
        if not self.power_manager.initialize():
            self.logger.warning("Power manager not available")

        self.logger.info("Module initialization complete")
        return True

    def handle_gps_update(self, location: dict):
        """Handle GPS location update"""
        device_id = self.config.get('device', {}).get('id', 'unknown')
        location['device_id'] = device_id

        # Store in buffer
        if self.data_buffer:
            self.data_buffer.insert_location(location)

        # Queue for Firebase sync
        if self.firebase_sync:
            self.firebase_sync.queue_data(location)

        self.logger.debug(f"GPS update: lat={location.get('latitude')}, lon={location.get('longitude')}")

    def graceful_shutdown(self):
        """Perform graceful shutdown"""
        self.logger.info("Initiating graceful shutdown...")

        # Flush any pending data
        if self.data_buffer:
            stats = self.data_buffer.get_stats()
            self.logger.info(f"Buffer stats: {stats}")

        # Stop all modules
        self.stop()

        self.logger.info("Graceful shutdown complete")

    def start(self):
        """Start the fleet tracker"""
        self.logger.info("Starting Fleet Tracker...")

        # Initialize modules
        if not self.initialize_modules():
            self.logger.error("Module initialization failed")
            return False

        self.running = True
        self.stop_event.clear()

        # Start GPS tracking
        if self.gps_tracker:
            self.gps_tracker.start_tracking(callback=self.handle_gps_update)

        # Start Firebase sync
        if self.firebase_sync:
            self.firebase_sync.start()

        # Start power monitoring
        if self.power_manager:
            self.power_manager.start(shutdown_callback=self.graceful_shutdown)

        self.logger.info("Fleet Tracker started successfully")

        # Main loop
        cleanup_interval = self.config.get('buffer', {}).get('cleanup_interval', 3600)
        last_cleanup = time.time()

        while self.running and not self.stop_event.is_set():
            try:
                # Periodic cleanup
                if time.time() - last_cleanup > cleanup_interval:
                    if self.data_buffer:
                        retention_days = self.config.get('buffer', {}).get('retention_days', 7)
                        self.data_buffer.cleanup_old_data(retention_days)
                    last_cleanup = time.time()

                # Health check
                self.health_check()

                # Wait for next iteration
                self.stop_event.wait(30)  # 30 second loop

            except KeyboardInterrupt:
                self.logger.info("Received interrupt signal")
                break
            except Exception as e:
                self.logger.error(f"Main loop error: {e}")

        return True

    def health_check(self):
        """Perform health check on all modules"""
        # Check GPS
        if self.gps_tracker and not self.gps_tracker.running:
            self.logger.warning("GPS tracker not running, attempting restart...")
            self.gps_tracker.start_tracking(callback=self.handle_gps_update)

        # Check Firebase
        if self.firebase_sync and not self.firebase_sync.running:
            self.logger.warning("Firebase sync not running, attempting restart...")
            self.firebase_sync.start()

        # Check Power
        if self.power_manager:
            status = self.power_manager.get_status()
            if status.get('capacity', 100) < 10:
                self.logger.warning(f"Battery critically low: {status.get('capacity')}%")

    def stop(self):
        """Stop the fleet tracker"""
        self.logger.info("Stopping Fleet Tracker...")
        self.running = False
        self.stop_event.set()

        # Stop all modules
        if self.gps_tracker:
            self.gps_tracker.stop_tracking()
            self.gps_tracker.close()

        if self.firebase_sync:
            self.firebase_sync.stop()

        if self.power_manager:
            self.power_manager.stop()

        if self.data_buffer:
            self.data_buffer.close()

        self.logger.info("Fleet Tracker stopped")

    def signal_handler(self, signum, frame):
        """Handle system signals"""
        self.logger.info(f"Received signal {signum}")
        self.stop()
        sys.exit(0)


def main():
    """Main entry point"""
    tracker = FleetTracker()

    # Setup signal handlers
    signal.signal(signal.SIGINT, tracker.signal_handler)
    signal.signal(signal.SIGTERM, tracker.signal_handler)

    # Start tracker
    try:
        tracker.start()
    except Exception as e:
        tracker.logger.error(f"Fatal error: {e}")
        tracker.stop()
        sys.exit(1)


if __name__ == '__main__':
    main()
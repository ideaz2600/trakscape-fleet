"""Configuration management for Trakscape Fleet Platform"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


class ConfigManager:
    """Manages application configuration"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.getenv(
            'FLEET_CONFIG',
            Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
        )
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'device': {
                'id': 'fleet-001',
                'name': 'Test Vehicle',
                'type': 'vehicle'
            },
            'gps': {
                'port': '/dev/ttyUSB2',
                'baudrate': 115200,
                'update_interval': 10,
                'timeout': 5,
                'min_satellites': 4
            },
            'cellular': {
                'apn': 'internet',
                'check_interval': 30,
                'reconnect_delay': 10
            },
            'firebase': {
                'project_id': 'trakscape-fleet',
                'credentials_path': 'config/firebase_key.json',
                'sync_interval': 30,
                'batch_size': 100,
                'compression': True
            },
            'power': {
                'i2c_address': 0x36,
                'low_battery_threshold': 20,
                'critical_battery_threshold': 5,
                'shutdown_delay': 60,
                'check_interval': 10
            },
            'buffer': {
                'database_path': 'data/buffer.db',
                'max_size_mb': 1000,
                'retention_days': 7,
                'cleanup_interval': 3600
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/fleet_tracker.log',
                'max_size_mb': 100,
                'backup_count': 5
            }
        }

    def get(self, key: str, default=None):
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def save(self):
        """Save current configuration to file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
"""Firebase synchronization module with offline buffering"""

import json
import gzip
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from threading import Thread, Event, Lock
import queue
import firebase_admin
from firebase_admin import credentials, db


class FirebaseSync:
    """Manages Firebase real-time database synchronization"""

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.sync_queue = queue.Queue()
        self.running = False
        self.stop_event = Event()
        self.sync_lock = Lock()
        self.app = None
        self.db_ref = None

    def initialize(self) -> bool:
        """Initialize Firebase connection"""
        try:
            cred = credentials.Certificate(self.config['credentials_path'])
            self.app = firebase_admin.initialize_app(cred, {
                'databaseURL': f"https://{self.config['project_id']}.firebaseio.com"
            })
            self.db_ref = db.reference()
            self.logger.info("Firebase initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Firebase initialization failed: {e}")
            return False

    def compress_data(self, data: Dict) -> bytes:
        """Compress data using gzip"""
        json_str = json.dumps(data)
        return gzip.compress(json_str.encode())

    def decompress_data(self, data: bytes) -> Dict:
        """Decompress gzip data"""
        json_str = gzip.decompress(data).decode()
        return json.loads(json_str)

    def queue_data(self, data: Dict):
        """Add data to sync queue"""
        self.sync_queue.put({
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
            'attempts': 0
        })

    def push_location(self, device_id: str, location: Dict) -> bool:
        """Push location update to Firebase"""
        try:
            # Current location
            current_ref = self.db_ref.child(f'vehicles/{device_id}/current_location')
            current_ref.set(location)

            # History (with timestamp as key)
            history_ref = self.db_ref.child(f'vehicles/{device_id}/history')
            timestamp = location.get('timestamp', datetime.utcnow().isoformat())
            history_ref.child(timestamp.replace('.', '_')).set(location)

            # Update device status
            status_ref = self.db_ref.child(f'vehicles/{device_id}/status')
            status_ref.update({
                'last_seen': timestamp,
                'online': True
            })

            self.logger.debug(f"Location pushed for {device_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to push location: {e}")
            return False

    def batch_upload(self, device_id: str, locations: List[Dict]) -> bool:
        """Upload multiple locations in batch"""
        try:
            if self.config.get('compression', True):
                # Compress batch
                compressed = self.compress_data({'locations': locations})
                size_reduction = (1 - len(compressed) / len(json.dumps(locations))) * 100
                self.logger.info(f"Compression saved {size_reduction:.1f}%")

            # Upload to history
            history_ref = self.db_ref.child(f'vehicles/{device_id}/history')
            batch_data = {}

            for location in locations:
                timestamp = location.get('timestamp', datetime.utcnow().isoformat())
                key = timestamp.replace('.', '_')
                batch_data[key] = location

            history_ref.update(batch_data)
            self.logger.info(f"Batch uploaded {len(locations)} locations")
            return True
        except Exception as e:
            self.logger.error(f"Batch upload failed: {e}")
            return False

    def sync_worker(self):
        """Background worker for syncing queued data"""
        batch = []
        last_sync = datetime.now()

        while self.running and not self.stop_event.is_set():
            try:
                # Get item from queue with timeout
                item = self.sync_queue.get(timeout=1)
                batch.append(item['data'])

                # Check if we should sync
                should_sync = (
                    len(batch) >= self.config.get('batch_size', 100) or
                    (datetime.now() - last_sync).seconds >= self.config.get('sync_interval', 30)
                )

                if should_sync and batch:
                    with self.sync_lock:
                        device_id = self.config.get('device_id', 'unknown')
                        if self.batch_upload(device_id, batch):
                            batch.clear()
                            last_sync = datetime.now()
                        else:
                            # Re-queue on failure
                            for data in batch:
                                self.sync_queue.put({
                                    'timestamp': datetime.utcnow().isoformat(),
                                    'data': data,
                                    'attempts': item.get('attempts', 0) + 1
                                })
                            batch.clear()

            except queue.Empty:
                # Timeout - check if we have pending batch
                if batch:
                    with self.sync_lock:
                        device_id = self.config.get('device_id', 'unknown')
                        if self.batch_upload(device_id, batch):
                            batch.clear()
                            last_sync = datetime.now()

            except Exception as e:
                self.logger.error(f"Sync worker error: {e}")

    def start(self):
        """Start sync service"""
        if not self.app:
            if not self.initialize():
                return False

        self.running = True
        self.stop_event.clear()
        Thread(target=self.sync_worker, daemon=True).start()
        self.logger.info("Firebase sync started")
        return True

    def stop(self):
        """Stop sync service"""
        self.running = False
        self.stop_event.set()
        self.logger.info("Firebase sync stopped")

    def get_device_config(self, device_id: str) -> Optional[Dict]:
        """Fetch device configuration from Firebase"""
        try:
            config_ref = self.db_ref.child(f'devices/{device_id}/config')
            return config_ref.get()
        except Exception as e:
            self.logger.error(f"Failed to fetch config: {e}")
            return None
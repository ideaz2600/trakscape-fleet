"""SQLite data buffering module for offline operation"""

import sqlite3
import json
import gzip
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from threading import Lock
import os


class DataBuffer:
    """Manages offline data buffering with SQLite"""

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.db_path = config.get('database_path', 'data/buffer.db')
        self.conn = None
        self.lock = Lock()

    def initialize(self) -> bool:
        """Initialize SQLite database"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.create_tables()
            self.logger.info(f"Data buffer initialized at {self.db_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize buffer: {e}")
            return False

    def create_tables(self):
        """Create database tables"""
        with self.lock:
            cursor = self.conn.cursor()

            # GPS data buffer
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gps_buffer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    device_id TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    speed REAL DEFAULT 0,
                    heading REAL DEFAULT 0,
                    altitude REAL DEFAULT 0,
                    satellites INTEGER DEFAULT 0,
                    hdop REAL DEFAULT 0,
                    synced BOOLEAN DEFAULT 0,
                    priority INTEGER DEFAULT 0,
                    compressed_data BLOB,
                    retry_count INTEGER DEFAULT 0
                )
            ''')

            # Create indexes
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_synced
                ON gps_buffer(synced, priority DESC, timestamp)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON gps_buffer(timestamp)
            ''')

            # Events buffer
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events_buffer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    device_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_data TEXT,
                    synced BOOLEAN DEFAULT 0,
                    priority INTEGER DEFAULT 0
                )
            ''')

            self.conn.commit()

    def insert_location(self, location: Dict, priority: int = 0) -> bool:
        """Insert location data into buffer"""
        try:
            with self.lock:
                cursor = self.conn.cursor()

                # Compress additional data
                extra_data = {k: v for k, v in location.items()
                             if k not in ['latitude', 'longitude', 'speed', 'heading', 'timestamp']}
                compressed = None
                if extra_data:
                    compressed = gzip.compress(json.dumps(extra_data).encode())

                cursor.execute('''
                    INSERT INTO gps_buffer (
                        device_id, latitude, longitude, speed, heading,
                        altitude, satellites, hdop, priority, compressed_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    location.get('device_id', 'unknown'),
                    location['latitude'],
                    location['longitude'],
                    location.get('speed', 0),
                    location.get('heading', 0),
                    location.get('altitude', 0),
                    location.get('satellites', 0),
                    location.get('hdop', 0),
                    priority,
                    compressed
                ))

                self.conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to insert location: {e}")
            return False

    def get_unsynced_batch(self, batch_size: int = 100) -> List[Dict]:
        """Get batch of unsynced data"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    SELECT * FROM gps_buffer
                    WHERE synced = 0 AND retry_count < 5
                    ORDER BY priority DESC, timestamp ASC
                    LIMIT ?
                ''', (batch_size,))

                rows = cursor.fetchall()
                results = []

                for row in rows:
                    data = {
                        'id': row['id'],
                        'timestamp': row['timestamp'],
                        'device_id': row['device_id'],
                        'latitude': row['latitude'],
                        'longitude': row['longitude'],
                        'speed': row['speed'],
                        'heading': row['heading'],
                        'altitude': row['altitude'],
                        'satellites': row['satellites'],
                        'hdop': row['hdop']
                    }

                    # Decompress additional data
                    if row['compressed_data']:
                        extra = json.loads(gzip.decompress(row['compressed_data']).decode())
                        data.update(extra)

                    results.append(data)

                return results
        except Exception as e:
            self.logger.error(f"Failed to get unsynced batch: {e}")
            return []

    def mark_synced(self, ids: List[int]) -> bool:
        """Mark records as synced"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                placeholders = ','.join('?' * len(ids))
                cursor.execute(f'''
                    UPDATE gps_buffer
                    SET synced = 1
                    WHERE id IN ({placeholders})
                ''', ids)
                self.conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to mark synced: {e}")
            return False

    def increment_retry(self, ids: List[int]) -> bool:
        """Increment retry count for failed sync"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                placeholders = ','.join('?' * len(ids))
                cursor.execute(f'''
                    UPDATE gps_buffer
                    SET retry_count = retry_count + 1
                    WHERE id IN ({placeholders})
                ''', ids)
                self.conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to increment retry: {e}")
            return False

    def cleanup_old_data(self, days: int = 7) -> int:
        """Remove old synced data"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cutoff_date = datetime.now() - timedelta(days=days)

                cursor.execute('''
                    DELETE FROM gps_buffer
                    WHERE synced = 1 AND timestamp < ?
                ''', (cutoff_date.isoformat(),))

                deleted = cursor.rowcount
                self.conn.commit()

                if deleted > 0:
                    self.logger.info(f"Cleaned up {deleted} old records")
                    # Vacuum to reclaim space
                    cursor.execute('VACUUM')

                return deleted
        except Exception as e:
            self.logger.error(f"Failed to cleanup data: {e}")
            return 0

    def get_stats(self) -> Dict:
        """Get buffer statistics"""
        try:
            with self.lock:
                cursor = self.conn.cursor()

                stats = {}

                # Total records
                cursor.execute('SELECT COUNT(*) as total FROM gps_buffer')
                stats['total'] = cursor.fetchone()['total']

                # Unsynced records
                cursor.execute('SELECT COUNT(*) as unsynced FROM gps_buffer WHERE synced = 0')
                stats['unsynced'] = cursor.fetchone()['unsynced']

                # Failed records (high retry count)
                cursor.execute('SELECT COUNT(*) as failed FROM gps_buffer WHERE retry_count >= 5')
                stats['failed'] = cursor.fetchone()['failed']

                # Database size
                cursor.execute('SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()')
                stats['size_bytes'] = cursor.fetchone()['size']

                return stats
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {}

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
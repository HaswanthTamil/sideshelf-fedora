import time
import threading
import logging
from .db import delete_older_than
from .config import TTL_SECONDS

logger = logging.getLogger(__name__)

class CleanupThread(threading.Thread):
    def __init__(self, interval_hours: int = 12):
        super().__init__(daemon=True)
        self.interval_seconds = interval_hours * 3600
        self.running = True

    def run(self):
        logger.info("Cleanup thread started.")
        while self.running:
            try:
                cutoff = int(time.time()) - TTL_SECONDS
                logger.info(f"Running cleanup for items older than {cutoff}")
                delete_older_than(cutoff)
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
            
            # Wait for the next interval, but check running flag periodically
            for _ in range(self.interval_seconds // 60):
                if not self.running:
                    break
                time.sleep(60)

    def stop(self):
        self.running = False

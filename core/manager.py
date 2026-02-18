from typing import List, Dict, Any, Callable
from .watcher import ClipboardWatcher
from ..storage import db
import logging

logger = logging.getLogger(__name__)

class ClipboardManager:
    def __init__(self):
        self.watcher = ClipboardWatcher(self.handle_new_item)
        self.on_items_changed_callbacks: List[Callable[[], None]] = []
        
        # Initialize DB
        db.init_db()

    def register_change_callback(self, callback: Callable[[], None]):
        self.on_items_changed_callbacks.append(callback)

    def handle_new_item(self, data: dict):
        logger.info(f"Handling new item: {data['id']} ({data['type']})")
        
        # In a real app, we might check for duplicates in DB here too
        # But watcher already does basic deduplication for text.
        
        try:
            db.insert_item(
                data['id'],
                data['type'],
                data['content'],
                data['created_at']
            )
            self._notify_ui()
        except Exception as e:
            logger.error(f"Failed to persist item: {e}")

    def _notify_ui(self):
        for callback in self.on_items_changed_callbacks:
            callback()

    def get_all_items(self) -> List[Dict[str, Any]]:
        return db.fetch_all_items()

    def delete_item(self, item_id: str):
        db.delete_item(item_id)
        self._notify_ui()

    def clear_all(self):
        db.clear_all()
        self._notify_ui()
        
    def copy_to_clipboard(self, item_id: str):
        item = db.get_item(item_id)
        if not item:
            return
            
        if item['type'] == 'text':
            self.watcher.set_text(item['content'])
        elif item['type'] == 'image':
            self.watcher.set_content_from_image_path(item['content'])

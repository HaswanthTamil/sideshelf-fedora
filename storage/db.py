import sqlite3
import os
import time
from typing import List, Dict, Any, Optional
from gi.repository import Gdk, GdkPixbuf
from .config import DB_PATH, IMAGE_DIR

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS clipboard_items (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at INTEGER NOT NULL
            )
        ''')
        conn.commit()

def insert_item(item_id: str, item_type: str, content: Any, created_at: int):
    """Insert a new clipboard item into the database."""
    if item_type == "image":
        # content is Gdk.Texture or similar, we need to save it as PNG
        file_path = IMAGE_DIR / f"{item_id}.png"
        save_texture_as_png(content, str(file_path))
        content_value = str(file_path)
    else:
        content_value = content

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO clipboard_items (id, type, content, created_at) VALUES (?, ?, ?, ?)",
            (item_id, item_type, content_value, created_at)
        )
        conn.commit()

def save_texture_as_png(texture: Gdk.Texture, path: str):
    """Saves a GdkTexture as a PNG file."""
    # Convert Texture to Pixbuf to save as PNG
    # Note: Gdk.Texture.save_to_png is available in GTK4 but might be easier via Pixbuf wrapper if needed
    # Let's try save_to_png first.
    texture.save_to_png(path)

def fetch_all_items() -> List[Dict[str, Any]]:
    """Fetch all clipboard items ordered by creation time DESC."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM clipboard_items ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def delete_item(item_id: str):
    """Delete an item and its associated image file if applicable."""
    item = get_item(item_id)
    if item and item['type'] == 'image':
        if os.path.exists(item['content']):
            os.remove(item['content'])
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM clipboard_items WHERE id = ?", (item_id,))
        conn.commit()

def get_item(item_id: str) -> Optional[Dict[str, Any]]:
    """Get a single item by ID."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM clipboard_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def delete_older_than(timestamp: int):
    """Delete entries and files older than the given timestamp."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT id, type, content FROM clipboard_items WHERE created_at < ?", (timestamp,))
        items_to_delete = cursor.fetchall()
        
        for item in items_to_delete:
            if item['type'] == 'image':
                if os.path.exists(item['content']):
                    os.remove(item['content'])
            conn.execute("DELETE FROM clipboard_items WHERE id = ?", (item['id'],))
        
        conn.commit()

def clear_all():
    """Clear all items and delete all image files."""
    items = fetch_all_items()
    for item in items:
        if item['type'] == 'image' and os.path.exists(item['content']):
            os.remove(item['content'])
            
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM clipboard_items")
        conn.commit()

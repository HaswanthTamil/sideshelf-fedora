import time
import uuid
from typing import Callable, Optional
from gi.repository import Gdk, GLib, Gio
import logging

logger = logging.getLogger(__name__)

class ClipboardWatcher:
    def __init__(self, callback: Callable[[dict], None]):
        self.callback = callback
        self.display = Gdk.Display.get_default()
        self.clipboard = self.display.get_clipboard()
        
        # Connect to the "changed" signal
        self.clipboard.connect("changed", self._on_clipboard_changed)
        
        # Track last processed item to avoid self-triggered loops or duplicates
        self.last_content_hash = None

    def _on_clipboard_changed(self, clipboard: Gdk.Clipboard):
        logger.info("Clipboard changed signal received.")
        
        formats = clipboard.get_formats()
        
        # Check for text first
        if formats.contain_mime_type("text/plain"):
            clipboard.read_text_async(None, self._on_text_read_finished)
        # Check for images
        elif formats.contain_mime_type("image/png") or formats.contain_mime_type("image/jpeg"):
            clipboard.read_texture_async(None, self._on_texture_read_finished)

    def _on_text_read_finished(self, clipboard: Gdk.Clipboard, result: Gio.AsyncResult):
        text = clipboard.read_text_finish(result)
        if text:
            content_hash = hash(text)
            if content_hash != self.last_content_hash:
                self.last_content_hash = content_hash
                item = {
                    "id": str(uuid.uuid4()),
                    "type": "text",
                    "content": text,
                    "created_at": int(time.time())
                }
                self.callback(item)

    def _on_texture_read_finished(self, clipboard: Gdk.Clipboard, result: Gio.AsyncResult):
        texture = clipboard.read_texture_finish(result)
        if texture:
            # For images, deduplication might be trickier, but let's at least avoid immediate duplicates
            # A simple hash of the texture object or some pixels could work.
            # For now, let's just emit it.
            item = {
                "id": str(uuid.uuid4()),
                "type": "image",
                "content": texture,
                "created_at": int(time.time())
            }
            self.callback(item)
            
    def set_text(self, text: str):
        """Programmatically set text to clipboard."""
        self.clipboard.set_text(text)

    def set_texture(self, texture: Gdk.Texture):
        """Programmatically set texture to clipboard."""
        self.clipboard.set_texture(texture)
        
    def set_content_from_image_path(self, path: str):
        """Load an image from path and set to clipboard."""
        file = Gio.File.new_for_path(path)
        texture = Gdk.Texture.new_from_file(file)
        self.clipboard.set_texture(texture)

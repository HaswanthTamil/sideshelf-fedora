from gi.repository import Gtk, Gdk, Gio
from typing import Any, Dict
from ..core.manager import ClipboardManager

class ClipboardPopup(Gtk.Window):
    def __init__(self, manager: ClipboardManager):
        super().__init__(title="SideShelf Clips")
        self.manager = manager
        self.set_default_size(350, 500)
        
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.main_box)
        
        # Scrolled Window
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_vexpand(True)
        self.main_box.append(self.scrolled)
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.scrolled.set_child(self.list_box)
        
        # Clear All Button
        clear_btn = Gtk.Button(label="Clear All")
        clear_btn.connect("clicked", self._on_clear_clicked)
        self.main_box.append(clear_btn)
        
        self.refresh()
        
        # Register for updates
        self.manager.register_change_callback(self.refresh)

    def refresh(self):
        # Clear existing rows
        while child := self.list_box.get_first_child():
            self.list_box.remove(child)
            
        items = self.manager.get_all_items()
        for item in items:
            row = self._create_row(item)
            self.list_box.append(row)

    def _create_row(self, item: Dict[str, Any]) -> Gtk.ListBoxRow:
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.set_margin_start(10)
        hbox.set_margin_end(10)
        hbox.set_margin_top(5)
        hbox.set_margin_bottom(5)
        row.set_child(hbox)
        
        # Preview
        if item['type'] == 'text':
            preview = Gtk.Label(label=item['content'][:50] + ("..." if len(item['content']) > 50 else ""))
            preview.set_halign(Gtk.Align.START)
            preview.set_ellipsize(3) # Pango.EllipsizeMode.END
            hbox.append(preview)
        else:
            # Image thumbnail
            image = Gtk.Image.new_from_file(item['content'])
            image.set_pixel_size(64)
            hbox.append(image)
            
        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        hbox.append(spacer)
        
        # Copy Button
        copy_btn = Gtk.Button(icon_name="edit-copy-symbolic")
        copy_btn.connect("clicked", lambda x: self.manager.copy_to_clipboard(item['id']))
        hbox.append(copy_btn)
        
        # Delete Button
        del_btn = Gtk.Button(icon_name="user-trash-symbolic")
        del_btn.connect("clicked", lambda x: self.manager.delete_item(item['id']))
        hbox.append(del_btn)
        
        return row

    def _on_clear_clicked(self, button):
        self.manager.clear_all()
        self.refresh()

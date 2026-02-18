from gi.repository import Gtk, Gio
from .popup import ClipboardPopup
from ..core.manager import ClipboardManager

class TrayIcon:
    """
    In GTK4, traditional tray icons (AppIndicator/StatusIcon) are deprecated or moved.
    However, for GNOME, we usually use Gtk.Application with a menu and an icon, 
    or libappindicator in some environments.
    For this scaffold, we'll use a simple approach: if we want a 'tray' behavior, 
    we might need libadwaita or just a window that stays hidden.
    
    Fedora usually supports AppIndicators via extensions. 
    A simpler GTK4 native way for a utility is to have a background app with a primary window 
    that toggles visibility.
    """
    def __init__(self, app: Gtk.Application, manager: ClipboardManager):
        self.app = app
        self.manager = manager
        self.popup = None

    def setup(self):
        # Create the popup window
        self.popup = ClipboardPopup(self.manager)
        self.app.add_window(self.popup)
        
        # In a real environment, you'd add an AppIndicator here.
        # For this scaffold, we'll just show the window on startup
        # and it can be closed/reopened via the app menu or similar.
        self.popup.present()

    def toggle_popup(self):
        if self.popup.get_visible():
            self.popup.hide()
        else:
            self.popup.present()

    def quit(self, *args):
        self.app.quit()

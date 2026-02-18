import sys
import logging
from gi.repository import Gtk, Gio, GLib
from sideshelf_pc.core.manager import ClipboardManager
from sideshelf_pc.ui.tray import TrayIcon
from sideshelf_pc.storage.cleanup import CleanupThread

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SideShelfPC")

class SideShelfApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.sideshelf.pc",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.manager = None
        self.tray = None
        self.cleanup = None

    def do_activate(self):
        if not self.manager:
            # Initialize Manager (starts internal watcher)
            self.manager = ClipboardManager()
            
            # Initialize Tray/UI
            self.tray = TrayIcon(self, self.manager)
            self.tray.setup()
            
            # Start Cleanup Thread
            self.cleanup = CleanupThread()
            self.cleanup.start()
            
            logger.info("SideShelf PC activated.")

    def do_startup(self):
        Gtk.Application.do_startup(self)
        
        # Create simple menu
        menu = Gio.Menu()
        menu.append("Quit", "app.quit")
        self.set_app_menu(menu)
        
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)

    def on_quit(self, action, parameter):
        if self.cleanup:
            self.cleanup.stop()
        self.quit()

def main():
    app = SideShelfApplication()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())

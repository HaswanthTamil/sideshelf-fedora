# SideShelf (Fedora Desktop)

A lightweight system tray clipboard manager for Fedora Linux.

Originally built as a personal utility.  
Now open-sourced for the Fedora / Wayland community.

Maintained by BytesBrush.

---

## Features

- Clipboard history (text + images)
- Stores multiple copied items
- Auto-delete after 7 days
- System tray popup UI
- Designed for Wayland (Fedora 43 tested)
- Works standalone (no Android required)

---

## Why?

Linux clipboard history is either:
- Too minimal  
- Too heavy  
- Or unreliable under Wayland  

SideShelf aims to be:

- Simple  
- Fast  
- Fedora-first  
- Local-only  

No cloud.  
No telemetry.  
No analytics.

---

## Architecture Overview

Core components:

- Clipboard listener
- Local storage with auto-expiry logic
- System tray / popup interface
- Wayland-compatible handling

Everything runs locally.

---

## Requirements

- Fedora 43+
- Wayland session
- Required system libraries (see build section)

---

## Build & Run

Clone the repository:

```bash
git clone https://github.com/BytesBrush/sideshelf-fedora.git
cd sideshelf-desktop
python3 main.py
```

---

## Storage Policy
- Clipboard items are stored locally.
- Items are automatically deleted after 7 days.
- No data leaves your machine.

---

## Roadmap
- Cross-device sync (Android companion)
- Encrypted local network transport
- File clipboard support
- Flatpak packaging
- Fedora COPR release

---

## Contributing
Pull requests are welcome.

---

Before contributing:
Open an issue to discuss major changes.
Keep changes minimal and focused.
Ensure Wayland compatibility.

---

## License
This project is licensed under the GNU General Public License v3.0 (GPLv3).
If you distribute modified versions, you must also distribute the source code under the same license.

---

## Disclaimer
This project is in active development.
Expect rough edges.

# Keyboard-Mouse Controller

An advanced keyboard and mouse controller that combines the strengths of two keyboard libraries (`keyboard` and `pynput`) for robust hotkey handling and mouse emulation.

## ✨ Features

- **Dual-library architecture**:
  - `keyboard` for system-wide hotkey suppression
  - `pynput` for shift-key support in hotkeys
- **Mouse emulation**:
  - Precise cursor movement with speed control
  - Mouse button simulation (left, right, middle)
  - Scroll wheel control
- **Intelligent hotkey system**:
  - Multiple modifier combinations
  - Turbo/slow modes for movement
  - Arrow key emulation with shift support
- **One-shot actions**:
  - Text operations (backspace, enter, end)
  - Arrow key sequences
  - Shift-modified arrow selections

## 🚀 Installation

### From source:

```bash
# Clone the repository
git clone https://github.com/script-logic/keyboard-mouse-controller.git
cd keyboard-mouse-controller

# Install with pip
pip install .
```

## ⚙️ Usage

### Basic usage:

Warning: The key registration works correctly only when the English keyboard layout is enabled at the moment the program is launched.

```python
from keyboard_mouse_controller import MyController, setup_configuration
from pynput.mouse import Controller as MouseController

mouse_controller = MouseController()
config = setup_configuration()
controller = MyController(config, mouse_controller)
controller.run()
```

### Project structure:

```
keyboard-mouse-controller/
├── pyproject.toml
├── README.md
└── key_controller.py
```

## 🔧 Configuration

The controller is highly configurable. Modify the `setup_configuration()` function in `config.py` to:

- Change activation keys
- Adjust movement speeds
- Remap mouse buttons
- Customize one-shot actions

## ⚠️ Requirements

- **Python 3.10 or higher**
- **Administrator/root privileges** (for global hotkey capture)
- **Linux**: `sudo` access for keyboard module
- **Windows**: Run as Administrator
- **macOS**: Accessibility permissions

## ⭐ Acknowledgments

- [keyboard](https://github.com/boppreh/keyboard) library for system-wide hotkey handling
- [pynput](https://github.com/moses-palmer/pynput) library for keyboard/mouse control
- All contributors and users of the project

---

**Note**: This tool requires appropriate permissions for keyboard interception. Use responsibly and only on systems you own or have permission to control.
```
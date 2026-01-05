"""
The key registration works correctly only when the English keyboard layout
is enabled at the moment the program is launched.
Using two different keyboard libraries for two reasons:
1. "keyboard" can suppress hotkeys from another applications
2. "pynput.keyboard" can assign suppressed "shift" to hotkeys in this app
"""

import time
import atexit
from itertools import combinations
from typing import Any, Callable, Dict

import keyboard
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key as KeyboardButton
from pynput.mouse import Button as MouseButton
from pynput.mouse import Controller as MouseController


class MyController:
    def __init__(
        self,
        config: Dict[str, Any],
        mouse_controller: MouseController,
    ):
        """Initializes all assigned keys, suppressed keys
        and starting conditions

        Args:
            config (Dict[str, Any]): dict with parameters and hotkeys
            mouse_controller (MouseController): object for processing
                mouse imitation
        """
        self.mouse_controller: MouseController = mouse_controller
        self.config: Dict[str, Any] = config
        self.is_running: bool = True
        self.current_movement: Dict[str, int] = {"dx": 0, "dy": 0}
        self.mouse_button_states: Dict[str, bool] = {}
        for action_key in self.config["mouse_button_actions"].keys():
            self.mouse_button_states[action_key] = False

        move_keys = list(self.config["mouse_move_keys"].keys())
        mouse_button_keys = list(self.config["mouse_button_actions"].keys())
        activation_key: str = self.config["activation_key"]
        activation_arrow_key_name: str = self.config["activation_arrow_key"]
        shift_arrow_imitation_name: str = self.config["shift_arrow_imitation"]
        turbo_key: str = self.config["turbo_key"]
        slow_key: str = self.config["slow_key"]

        self._register_hotkey([self.config["exit_key"]], self.stop)

        self._register_action_hotkeys(
            self.config["one_shot_actions"], activation_key
        )

        self._register_action_hotkeys(
            self.config["one_shot_arrows"], activation_arrow_key_name
        )

        self._register_action_hotkeys(
            self.config["one_shot_arrows_shift"],
            [activation_arrow_key_name, shift_arrow_imitation_name],
        )

        self._register_hotkey(
            [activation_arrow_key_name, shift_arrow_imitation_name]
        )

        self._register_arrow_combinations(
            self.config["one_shot_arrows"], activation_arrow_key_name
        )

        self._register_arrow_combinations(
            self.config["one_shot_arrows_shift"],
            [activation_arrow_key_name, shift_arrow_imitation_name],
        )

        for key_name in mouse_button_keys:
            self._register_hotkey([activation_key, key_name])

        self._register_movement_combinations(
            move_keys, mouse_button_keys, activation_key, turbo_key, slow_key
        )

        self._register_triple_movement_combinations(
            move_keys, activation_key, turbo_key, slow_key
        )

        print(
            """The key registration works correctly only when the English \n
            keyboard layout is enabled at the moment the program is launched"""
        )

        atexit.register(self._cleanup)

    def _register_hotkey(
        self,
        keys: str | list[str],
        action_func: Callable = lambda: None,
        suppress: bool = True,
    ) -> str:
        """Main function for forming name of full combination and
        registering it with "keyboard" library

        Args:
            keys (str | list[str]): buttons names.
            action_func (Callable, optional): callable function by this keys
                combination. Defaults to lambda: None.
            suppress (bool, optional): evading sending hotkeys to other
                applications. Defaults to True.

        Returns:
            str: full name of registered combination
        """
        if isinstance(keys, str):
            keys = [keys]

        hotkey = "+".join(keys)

        keyboard.add_hotkey(hotkey, action_func, suppress=suppress)

        print(f"Hotkey registered: {hotkey}")
        return hotkey

    def _register_action_hotkeys(self, actions, activation_keys):

        if isinstance(activation_keys, str):
            activation_keys = [activation_keys]

        for key_name, action_func in actions.items():
            self._register_hotkey([*activation_keys, key_name], action_func)

    def _register_arrow_combinations(self, arrows, activation_keys):

        if isinstance(activation_keys, str):
            activation_keys = [activation_keys]

        arrow_keys = list(arrows.keys())
        for key1, key2 in combinations(arrow_keys, 2):
            self._register_hotkey([*activation_keys, key1, key2])

    def _register_movement_combinations(
        self, move_keys, mouse_button_keys, activation_key, turbo_key, slow_key
    ):

        modifiers = [[], [turbo_key], [slow_key]]

        for key in move_keys:
            for modifier in modifiers:
                self._register_hotkey([activation_key, key, *modifier])

            for mouse_key in mouse_button_keys:
                for modifier in modifiers:
                    self._register_hotkey(
                        [activation_key, key, mouse_key, *modifier]
                    )

        for key1, key2 in combinations(move_keys, 2):
            for modifier in modifiers:
                self._register_hotkey([activation_key, key1, key2, *modifier])

            for mouse_key in mouse_button_keys:
                for modifier in modifiers:
                    self._register_hotkey(
                        [activation_key, key1, key2, mouse_key, *modifier]
                    )

        for mouse_key in mouse_button_keys:
            for modifier in [turbo_key, slow_key]:
                self._register_hotkey([activation_key, mouse_key, modifier])

    def _register_triple_movement_combinations(
        self, move_keys, activation_key, turbo_key, slow_key
    ):

        modifiers = [[], [turbo_key], [slow_key]]

        for key1, key2, key3 in combinations(move_keys, 3):
            for modifier in modifiers:
                self._register_hotkey(
                    [activation_key, key1, key2, key3, *modifier]
                )

    def _process_mouse_buttons(self):
        """Imitates mouse buttons clicks"""
        if not keyboard.is_pressed(self.config["activation_key"]):
            for action_key, button_info in self.config[
                "mouse_button_actions"
            ].items():
                if self.mouse_button_states[action_key]:
                    self.mouse_button_states[action_key] = False
                    self.mouse_controller.release(button_info["button"])
                    print(f"Button released: {button_info['name']}")
                    print(f"mouse_button_states {self.mouse_button_states}")
            return

        for action_key, button_info in self.config[
            "mouse_button_actions"
        ].items():
            should_be_pressed = keyboard.is_pressed(action_key)
            currently_pressed = self.mouse_button_states[action_key]

            if should_be_pressed and not currently_pressed:
                self.mouse_button_states[action_key] = True
                self.mouse_controller.press(button_info["button"])
                print(f"Button pressed: {button_info['name']}")
                print(f"mouse_button_states {self.mouse_button_states}")

            elif not should_be_pressed and currently_pressed:
                self.mouse_button_states[action_key] = False
                self.mouse_controller.release(button_info["button"])
                print(f"Button released: {button_info['name']}")
                print(f"mouse_button_states {self.mouse_button_states}")

    def _process_continuous_actions(self):
        """Imitates mouse movement"""
        if not keyboard.is_pressed(self.config["activation_key"]):
            return

        dx, dy = 0, 0
        for key_name, (step_x, step_y) in self.config[
            "mouse_move_keys"
        ].items():
            if keyboard.is_pressed(key_name):
                dx += step_x
                dy += step_y

        if dx != 0 or dy != 0:
            is_turbo_mode = keyboard.is_pressed(self.config["turbo_key"])
            is_slow_mode = keyboard.is_pressed(self.config["slow_key"])

            speed = self.config["move_pixels"]
            if is_turbo_mode:
                speed *= self.config["turbo_multiplier"]
            if is_slow_mode:
                speed /= self.config["slow_divisor"]

            self.mouse_controller.move(int(dx * speed), int(dy * speed))

    def _cleanup(self):
        print("Cleanup...")

        for action_key, button_info in self.config[
            "mouse_button_actions"
        ].items():
            if self.mouse_button_states.get(action_key, False):
                self.mouse_controller.release(button_info["button"])
                self.mouse_button_states[action_key] = False

        try:
            keyboard.unhook_all()
        except Exception:
            pass

        print("✓ Cleanup completed")

    def stop(self):
        """Stops controller"""
        print("Stop...")
        self.is_running = False
        self._cleanup()

    def run(self):
        """
        Main controller cycle, that processes all keys while program
        running and releases them on exit.
        """
        try:
            print("Started. Press HOME for exit.")
            while self.is_running:
                self._process_mouse_buttons()
                self._process_continuous_actions()
                time.sleep(self.config["loop_delay"])

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            self.stop()

        except Exception as e:
            print(f"\n❌ Main cycle error: {e}")
            import traceback

            traceback.print_exc()
            self.stop()

        finally:
            self._cleanup()


def setup_configuration():
    def perform_backspace():
        print("backspace (press_and_release)")
        keyboard.press_and_release("backspace")

    def perform_enter():
        print("enter (press_and_release)")
        keyboard.press_and_release("enter")

    def perform_commenting():
        print("ctrl+/ (press_and_release)")
        with keyboard_controller.pressed(KeyboardButton.ctrl_r):
            keyboard_controller.press("/")
            keyboard_controller.release("/")

    def perform_scrollup():
        print(f"scrollup ({config['scroll_units']} units)")
        mouse_controller.scroll(0, dy=config["scroll_units"])

    def perform_scrolldown():
        print(f"scrolldown ({config['scroll_units']} units)")
        mouse_controller.scroll(0, dy=-config["scroll_units"])

    def perform_up():
        print("up (press_and_release)")
        keyboard.press_and_release("up")
        keyboard.press_and_release(config["activation_arrow_key"])

    def perform_down():
        print("down (press_and_release)")
        keyboard.press_and_release("down")
        keyboard.press_and_release(config["activation_arrow_key"])

    def perform_left():
        print("left (press_and_release)")
        keyboard.press_and_release("left")
        keyboard.press_and_release(config["activation_arrow_key"])

    def perform_right():
        print("right (press_and_release)")
        keyboard.press_and_release("right")
        keyboard.press_and_release(config["activation_arrow_key"])

    def perform_end():
        print("end (press_and_release)")
        keyboard.press_and_release("end")

    def perform_down_shift():
        print("down+shift (press_and_release)")
        with keyboard_controller.pressed(KeyboardButton.shift_r):
            keyboard_controller.press(KeyboardButton.down)
            keyboard_controller.release(KeyboardButton.down)

    def perform_left_shift():
        print("left+shift (press_and_release)")
        with keyboard_controller.pressed(KeyboardButton.shift_r):
            keyboard_controller.press(KeyboardButton.left)
            keyboard_controller.release(KeyboardButton.left)

    def perform_right_shift():
        print("right+shift (press_and_release)")
        with keyboard_controller.pressed(KeyboardButton.shift_r):
            keyboard_controller.press(KeyboardButton.right)
            keyboard_controller.release(KeyboardButton.right)

    def perform_up_shift():
        print("up+shift (press_and_release)")
        with keyboard_controller.pressed(KeyboardButton.shift_r):
            keyboard_controller.press(KeyboardButton.up)
            keyboard_controller.release(KeyboardButton.up)

    config = {
        "activation_key": "left ctrl",
        "activation_arrow_key": "left shift",
        "shift_arrow_imitation": "space",
        "turbo_key": "space",
        "slow_key": "left alt",
        "exit_key": "home",
        "move_pixels": 5,
        "turbo_multiplier": 7,
        "slow_divisor": 2,
        "scroll_units": 2,
        "mouse_move_keys": {
            "i": (0, -1),
            "k": (0, 1),
            "j": (-1, 0),
            "l": (1, 0),
        },
        "mouse_button_actions": {
            "semicolon": {"name": "lmb", "button": MouseButton.left},
            "'": {"name": "rmb", "button": MouseButton.right},
            "slash": {"name": "mmb", "button": MouseButton.middle},
        },
        "one_shot_actions": {
            "n": perform_scrollup,
            "m": perform_scrolldown,
            "h": perform_backspace,
            "u": perform_enter,
            "o": perform_end,
            "p": perform_commenting,
        },
        "one_shot_arrows": {
            "e": perform_up,
            "d": perform_down,
            "s": perform_left,
            "f": perform_right,
        },
        "one_shot_arrows_shift": {
            "e": perform_up_shift,
            "d": perform_down_shift,
            "s": perform_left_shift,
            "f": perform_right_shift,
        },
        "loop_delay": 0.01,
    }
    return config


if __name__ == "__main__":
    controller = None
    try:
        keyboard_controller = KeyboardController()
        mouse_controller = MouseController()
        configuration = setup_configuration()
        controller = MyController(configuration, mouse_controller)

        controller.run()

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        if controller:
            controller.stop()

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback

        traceback.print_exc()
        if controller:
            controller.stop()

    finally:
        print("\nExit...")

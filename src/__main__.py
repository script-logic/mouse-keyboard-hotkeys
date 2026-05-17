import logging
import sys
import time
from collections.abc import Callable
from enum import Enum, StrEnum
from itertools import combinations

import keyboard
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key as KeyboardButton
from pynput.mouse import Button as MouseButton
from pynput.mouse import Controller as MouseController

logging.basicConfig()
log = logging.getLogger("")
log.setLevel(logging.INFO)


class Keys(StrEnum):
    activation_key = "left ctrl"
    activation_arrow_key = "left shift"
    shift_arrow_imitation = "space"
    turbo_key = "space"
    slow_key = "left alt"
    exit_key = "home"
    mouse_move_up = "i"
    mouse_move_down = "k"
    mouse_move_left = "j"
    mouse_move_right = "l"
    mouse_click_left = "semicolon"
    mouse_click_middle = "'"
    mouse_click_right = "slash"
    scrollup = "n"
    scrolldown = "m"
    backspace = "h"
    enter = "u"
    end = "o"
    commenting = "p"
    up = "e"
    down = "d"
    left = "s"
    right = "f"
    up_shift = "e"
    down_shift = "d"
    left_shift = "s"
    right_shift = "f"


class Config(Enum):
    move_pixels_at_once = 5
    turbo_multiplier = 7
    slow_divisor = 2
    scroll_units = 3
    loop_delay = 0.01
    tries = 4


def perform_backspace() -> None:
    log.debug("perform_backspace")
    keyboard.press_and_release("backspace")


def perform_enter() -> None:
    log.debug("perform_enter")
    keyboard.press_and_release("enter")


def perform_commenting() -> None:
    log.debug("perform_commenting")
    with keyboard_controller.pressed(KeyboardButton.ctrl_r):
        keyboard_controller.press("/")
        keyboard_controller.release("/")


def perform_scrollup() -> None:
    log.debug("perform_scrollup")
    mouse_controller.scroll(0, dy=Config.scroll_units.value)


def perform_scrolldown() -> None:
    log.debug("perform_scrolldown")
    mouse_controller.scroll(0, dy=-Config.scroll_units.value)


def perform_up() -> None:
    log.debug("perform_up")
    keyboard.press_and_release("up")
    keyboard.press_and_release(Keys.activation_arrow_key.value)


def perform_down() -> None:
    log.debug("perform_down")
    keyboard.press_and_release("down")
    keyboard.press_and_release(Keys.activation_arrow_key.value)


def perform_left() -> None:
    log.debug("perform_left")
    keyboard.press_and_release("left")
    keyboard.press_and_release(Keys.activation_arrow_key.value)


def perform_right() -> None:
    log.debug("perform_right")
    keyboard.press_and_release("right")
    keyboard.press_and_release(Keys.activation_arrow_key.value)


def perform_end() -> None:
    log.debug("perform_end")
    keyboard.press_and_release("end")


def perform_down_shift() -> None:
    log.debug("perform_down_shift")
    with keyboard_controller.pressed(KeyboardButton.shift_r):
        keyboard_controller.press(KeyboardButton.down)
        keyboard_controller.release(KeyboardButton.down)


def perform_left_shift() -> None:
    log.debug("perform_left_shift")
    with keyboard_controller.pressed(KeyboardButton.shift_r):
        keyboard_controller.press(KeyboardButton.left)
        keyboard_controller.release(KeyboardButton.left)


def perform_right_shift() -> None:
    log.debug("perform_right_shift")
    with keyboard_controller.pressed(KeyboardButton.shift_r):
        keyboard_controller.press(KeyboardButton.right)
        keyboard_controller.release(KeyboardButton.right)


def perform_up_shift() -> None:
    log.debug("perform_up_shift")
    with keyboard_controller.pressed(KeyboardButton.shift_r):
        keyboard_controller.press(KeyboardButton.up)
        keyboard_controller.release(KeyboardButton.up)


class MouseMoveActions(Enum):
    mouse_move_up = (0, -1)
    mouse_move_down = (0, 1)
    mouse_move_left = (-1, 0)
    mouse_move_right = (1, 0)


class MouseButtonActions(Enum):
    mouse_click_left = MouseButton.left
    mouse_click_middle = MouseButton.middle
    mouse_click_right = MouseButton.right


ONE_SHOT_ACTIONS = {
    "scrollup": perform_scrollup,
    "scrolldown": perform_scrolldown,
    "backspace": perform_backspace,
    "enter": perform_enter,
    "end": perform_end,
    "commenting": perform_commenting,
}

ONE_SHOT_ARROWS = {
    "up": perform_up,
    "down": perform_down,
    "left": perform_left,
    "right": perform_right,
}

ONE_SHOT_ARROWS_SHIFT = {
    "up_shift": perform_up_shift,
    "down_shift": perform_down_shift,
    "left_shift": perform_left_shift,
    "right_shift": perform_right_shift,
}


class HooksRegistry:
    def __init__(self) -> None:
        self.register_hotkey([Keys.exit_key], cleanup)
        self.register_action_hotkeys()
        self.register_arrow_combinations_for_suppress()
        self.register_movement_combinations_suppress()
        self.register_triple_movement_combinations_suppress()
        self.register_hotkey([
            Keys.activation_arrow_key,
            Keys.shift_arrow_imitation,
        ])
        for key in MouseButtonActions:
            self.register_hotkey([Keys.activation_key, Keys[key.name]])

    @staticmethod
    def register_hotkey[T: bool | None](
        keys: list[str],
        action_func: Callable[..., T] = lambda: None,
        *,
        suppress: bool = True,
    ) -> None:

        hotkey = "+".join(keys)
        keyboard.add_hotkey(hotkey, action_func, suppress=suppress)
        log.info("Hotkey registered: %s", hotkey)
        log.info("Func registered: %s", action_func)

    def register_action_hotkeys(self) -> None:

        for key, action in ONE_SHOT_ACTIONS.items():
            self.register_hotkey(
                [Keys[key].value, Keys.activation_key], action
            )
        for key, action in ONE_SHOT_ARROWS.items():
            self.register_hotkey(
                [Keys[key].value, Keys.activation_arrow_key],
                action,
            )
        for key, action in ONE_SHOT_ARROWS_SHIFT.items():
            self.register_hotkey(
                [
                    Keys[key].value,
                    Keys.activation_arrow_key,
                    Keys.shift_arrow_imitation,
                ],
                action,
            )

    def register_arrow_combinations_for_suppress(self) -> None:

        for key1, key2 in combinations(ONE_SHOT_ARROWS, 2):
            self.register_hotkey([
                Keys.activation_arrow_key,
                Keys[key1],
                Keys[key2],
            ])

        for key1, key2, key3 in combinations(ONE_SHOT_ARROWS, 3):
            self.register_hotkey([
                Keys.activation_arrow_key,
                Keys[key1],
                Keys[key2],
                Keys[key3],
            ])

        for key1, key2 in combinations(ONE_SHOT_ARROWS_SHIFT, 2):
            self.register_hotkey([
                Keys.activation_arrow_key,
                Keys.shift_arrow_imitation,
                Keys[key1],
                Keys[key2],
            ])

        for key1, key2, key3 in combinations(ONE_SHOT_ARROWS_SHIFT, 3):
            self.register_hotkey([
                Keys.activation_arrow_key,
                Keys.shift_arrow_imitation,
                Keys[key1],
                Keys[key2],
                Keys[key3],
            ])

    def register_movement_combinations_suppress(self) -> None:  # noqa: C901

        modifiers = [[], [Keys.turbo_key], [Keys.slow_key]]

        for key in MouseMoveActions:
            for modifier in modifiers:
                self.register_hotkey([
                    Keys.activation_key,
                    Keys[key.name].value,
                    *modifier,
                ])

            for mouse_key in MouseButtonActions:
                for modifier in modifiers:
                    self.register_hotkey([
                        Keys.activation_key,
                        Keys[key.name].value,
                        Keys[mouse_key.name].value,
                        *modifier,
                    ])
        move_keys = [x.name for x in MouseMoveActions]
        for key1, key2 in combinations(move_keys, 2):
            for modifier in modifiers:
                self.register_hotkey([
                    Keys.activation_key,
                    Keys[key1],
                    Keys[key2],
                    *modifier,
                ])

            for mouse_key in MouseButtonActions:
                for modifier in modifiers:
                    self.register_hotkey([
                        Keys.activation_key,
                        Keys[key1],
                        Keys[key2],
                        Keys[mouse_key.name].value,
                        *modifier,
                    ])

        for mouse_key in MouseButtonActions:
            for modifier in [Keys.turbo_key, Keys.slow_key]:
                self.register_hotkey([
                    Keys.activation_key,
                    Keys[mouse_key.name].value,
                    modifier,
                ])

    def register_triple_movement_combinations_suppress(self) -> None:

        modifiers = [[], [Keys.turbo_key], [Keys.slow_key]]

        move_keys = [x.name for x in MouseMoveActions]
        for key1, key2, key3 in combinations(move_keys, 3):
            for modifier in modifiers:
                self.register_hotkey([
                    Keys.activation_key,
                    Keys[key1],
                    Keys[key2],
                    Keys[key3],
                    *modifier,
                ])


def cleanup(tries: int = 0) -> None:
    global is_running  # noqa: PLW0603
    tries += 1
    log.info("Cleanup...")
    try:
        keyboard.unhook_all()

        for mouse_button in mouse_button_pressed.copy():
            mouse_controller.release(mouse_button)
            mouse_button_pressed.remove(mouse_button)

    except Exception:
        log.exception("X Cleanup error, try: %s", tries)
        if tries < Config.tries.value:
            cleanup(tries)
        log.info("X FATAL Cleanup error")

    log.info("mouse_button_pressed: %s", mouse_button_pressed)
    log.info("✓ Cleanup completed")
    log.info("Exit...")
    is_running = False


def process_mouse_buttons() -> None:
    if not keyboard.is_pressed(activation_key):
        for button in mouse_buttons:
            if button in mouse_button_pressed:
                mouse_button_pressed.discard(button)
                mouse_controller.release(button)
                log.debug("Button released: %s", button)
        return

    for button in mouse_buttons:
        action = MouseButtonActions(button).name
        should_be_pressed: bool = keyboard.is_pressed(Keys[action].value)
        currently_pressed = button in mouse_button_pressed

        if should_be_pressed and not currently_pressed:
            mouse_button_pressed.add(button)
            mouse_controller.press(button)
            log.debug("Button pressed: %s", action)

        elif (not should_be_pressed) and currently_pressed:
            mouse_button_pressed.discard(button)
            mouse_controller.release(button)
            log.debug("Button released: %s", action)


def process_continuous_actions() -> None:

    for action in mouse_move_actions:
        if keyboard.is_pressed(Keys[action]):
            speed = (
                turbo_speed
                if keyboard.is_pressed(turbo_key)
                else slow_speed
                if keyboard.is_pressed(slow_key)
                else default_speed
            )
            mouse_controller.move(
                MouseMoveActions[action].value[0] * speed,
                MouseMoveActions[action].value[1] * speed,
            )


keyboard_controller: KeyboardController = KeyboardController()
mouse_controller: MouseController = MouseController()
is_running: bool = True
current_movement: dict[str, int] = {"dx": 0, "dy": 0}
mouse_button_pressed: set[MouseButton] = set()
default_speed: int = Config.move_pixels_at_once.value
mouse_move_actions: tuple[str, ...] = tuple(x.name for x in MouseMoveActions)
slow_speed = int(Config.move_pixels_at_once.value / Config.slow_divisor.value)
HooksRegistry()
loop_delay: float = Config.loop_delay.value
activation_key: str = Keys.activation_key
turbo_key: str = Keys.turbo_key
slow_key: str = Keys.slow_key
mouse_buttons: tuple[MouseButton, ...] = tuple(
    x.value for x in MouseButtonActions
)
turbo_speed = int(
    Config.move_pixels_at_once.value * Config.turbo_multiplier.value
)
try:
    while is_running:
        process_mouse_buttons()

        if keyboard.is_pressed(activation_key):
            process_continuous_actions()

        time.sleep(loop_delay)

    log.info("Program terminated normally")
    sys.exit(0)

except KeyboardInterrupt:
    log.info("KeyboardInterrupt received")
    cleanup()
    sys.exit(0)

except Exception:
    log.exception("Unexpected exception")
    cleanup()
    sys.exit(1)

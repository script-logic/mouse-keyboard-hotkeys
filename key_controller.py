import time
import keyboard
from pynput import mouse
from itertools import combinations


class MouseKeyController:
    def __init__(self, config):
        self.config = config
        self.mouse_controller = mouse.Controller()
        self.is_running = True
        self.current_movement = {'dx': 0, 'dy': 0}
        
        # Состояние кнопок мыши (зажаты или нет)
        self.mouse_button_states = {}
        for action_key in self.config['mouse_button_actions'].keys():
            self.mouse_button_states[action_key] = False
            
        self._setup_hotkeys()

    def _setup_hotkeys(self):
        """Регистрирует все горячие клавиши."""
        # Регистрируем клавишу выхода
        keyboard.add_hotkey(
            self.config['exit_key'], 
            self.stop, 
            suppress=True
        )

        activation_key_name = self.config['activation_key']
        activation_arrow_key_name = self.config['activation_arrow_key']
        
        # Регистрируем одноразовые действия (не кнопки мыши)
        for key_name, action_func in self.config['one_shot_actions'].items():
            hotkey_string = f"{activation_key_name}+{key_name}"
            keyboard.add_hotkey(hotkey_string, action_func, suppress=True)
            print(f"Зарегистрирован хоткей: {hotkey_string}")

        # Регистрируем стрелки (не кнопки мыши)
        for key_name, action_func in self.config['one_shot_arrows'].items():
            hotkey_string = f"{activation_arrow_key_name}+{key_name}"
            keyboard.add_hotkey(hotkey_string, action_func, suppress=True)
            print(f"Зарегистрирован хоткей: {hotkey_string}")

        arrow_keys = list(self.config['one_shot_arrows'].keys())
        for key1, key2 in combinations(arrow_keys, 2):
            hotkey = f"{activation_arrow_key_name}+{key1}+{key2}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")

        # Регистрируем хоткеи для кнопок мыши (только для подавления)
        for key_name in self.config['mouse_button_actions'].keys():
            hotkey_string = f"{activation_key_name}+{key_name}"
            keyboard.add_hotkey(hotkey_string, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей кнопки мыши: {hotkey_string}")

        # Получаем все клавиши движения
        move_keys = list(self.config['mouse_move_keys'].keys())
        mouse_button_keys = list(self.config['mouse_button_actions'].keys())
        turbo_key = self.config['turbo_key']
        slow_key = self.config['slow_key']
        
        # Регистрируем все возможные комбинации
        self._register_all_combinations(activation_key_name, move_keys, mouse_button_keys, turbo_key, slow_key)

    def _register_all_combinations(self, activation_key, move_keys, mouse_button_keys, turbo_key, slow_key):
        """Регистрирует все возможные комбинации клавиш."""
        
        # Регистрируем одиночные клавиши движения
        for key in move_keys:
            hotkey = f"{activation_key}+{key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            hotkey = f"{activation_key}+{key}+{turbo_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            hotkey = f"{activation_key}+{key}+{slow_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            # Комбинации движения с кнопками мыши
            for mouse_key in mouse_button_keys:
                hotkey = f"{activation_key}+{key}+{mouse_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей: {hotkey}")
                
                hotkey = f"{activation_key}+{key}+{mouse_key}+{turbo_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей: {hotkey}")
                
                hotkey = f"{activation_key}+{key}+{mouse_key}+{slow_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей: {hotkey}")
        
        # Регистрируем парные комбинации движения (диагонали)
        for key1, key2 in combinations(move_keys, 2):
            hotkey = f"{activation_key}+{key1}+{key2}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            hotkey = f"{activation_key}+{key1}+{key2}+{turbo_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            hotkey = f"{activation_key}+{key1}+{key2}+{slow_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            # Комбинации диагонального движения с кнопками мыши
            for mouse_key in mouse_button_keys:
                hotkey = f"{activation_key}+{key1}+{key2}+{mouse_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей: {hotkey}")
                
                hotkey = f"{activation_key}+{key1}+{key2}+{mouse_key}+{turbo_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей: {hotkey}")
                
                hotkey = f"{activation_key}+{key1}+{key2}+{mouse_key}+{slow_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей: {hotkey}")

        # Регистрируем комбинации только кнопок мыши с модификаторами
        for mouse_key in mouse_button_keys:
            hotkey = f"{activation_key}+{mouse_key}+{turbo_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей: {hotkey}")
            
            hotkey = f"{activation_key}+{mouse_key}+{slow_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей: {hotkey}")

        # Регистрируем тройные комбинации движения
        for key1, key2, key3 in combinations(move_keys, 3):
            hotkey = f"{activation_key}+{key1}+{key2}+{key3}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            hotkey = f"{activation_key}+{key1}+{key2}+{key3}+{turbo_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
            
            hotkey = f"{activation_key}+{key1}+{key2}+{key3}+{slow_key}"
            keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
            print(f"Зарегистрирован хоткей движения: {hotkey}")
        
        # И четверные комбинации движения (все клавиши одновременно)
        if len(move_keys) >= 4:
            for key1, key2, key3, key4 in combinations(move_keys, 4):
                hotkey = f"{activation_key}+{key1}+{key2}+{key3}+{key4}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей движения: {hotkey}")
                
                hotkey = f"{activation_key}+{key1}+{key2}+{key3}+{key4}+{turbo_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей движения: {hotkey}")
                
                hotkey = f"{activation_key}+{key1}+{key2}+{key3}+{key4}+{slow_key}"
                keyboard.add_hotkey(hotkey, lambda: None, suppress=True)
                print(f"Зарегистрирован хоткей движения: {hotkey}")

    def _process_mouse_buttons(self):
        """Обрабатывает состояние кнопок мыши (зажатие/отжатие)."""
        # Если Ctrl не зажат, отжимаем все кнопки мыши
        if not keyboard.is_pressed(self.config['activation_key']):
            for action_key, button_info in self.config['mouse_button_actions'].items():
                if self.mouse_button_states[action_key]:
                    self.mouse_button_states[action_key] = False
                    self.mouse_controller.release(button_info['button'])
                    print(f"Отжата кнопка: {button_info['name']}")
            return

        # Проверяем каждую кнопку мыши
        for action_key, button_info in self.config['mouse_button_actions'].items():
            should_be_pressed = keyboard.is_pressed(action_key)
            currently_pressed = self.mouse_button_states[action_key]
            
            if should_be_pressed and not currently_pressed:
                # Нужно зажать кнопку
                self.mouse_button_states[action_key] = True
                self.mouse_controller.press(button_info['button'])
                print(f"Зажата кнопка: {button_info['name']}")
                
            elif not should_be_pressed and currently_pressed:
                # Нужно отжать кнопку
                self.mouse_button_states[action_key] = False
                self.mouse_controller.release(button_info['button'])
                print(f"Отжата кнопка: {button_info['name']}")

    def _process_continuous_actions(self):
        """Обрабатывает продолжительные действия (движение мыши)."""
        
        # Если Ctrl не зажат, ничего не делаем
        if not keyboard.is_pressed(self.config['activation_key']):
            return

        # Пересчитываем текущее движение на основе нажатых клавиш
        dx, dy = 0, 0
        for key_name, (step_x, step_y) in self.config['mouse_move_keys'].items():
            if keyboard.is_pressed(key_name):
                dx += step_x
                dy += step_y

        if dx != 0 or dy != 0:
            is_turbo_mode = keyboard.is_pressed(self.config['turbo_key'])
            is_slow_mode = keyboard.is_pressed(self.config['slow_key'])
            
            speed = self.config['move_pixels']
            if is_turbo_mode:
                speed *= self.config['turbo_multiplier']
            if is_slow_mode:
                speed /= self.config['slow_divisor']
            
            self.mouse_controller.move(int(dx * speed), int(dy * speed))

    def stop(self):
        print("Клавиша выхода нажата. Завершение работы...")
        # Отжимаем все кнопки мыши перед выходом
        for action_key, button_info in self.config['mouse_button_actions'].items():
            if self.mouse_button_states[action_key]:
                self.mouse_controller.release(button_info['button'])
                print(f"Отжата кнопка при выходе: {button_info['name']}")
        self.is_running = False

    def run(self):
        print("="*60)
        print("Контроллер мыши активен.")
        print("Левый CTRL для активации функций движения и клика")
        print(f"-> Движение: I, J, K, L (только с зажатым Ctrl)")
        print(f"-> ВЫХОД: {self.config['exit_key'].upper()} (работает всегда)")
        print("="*60)

        try:
            while self.is_running:
                self._process_mouse_buttons() 
                self._process_continuous_actions()  # Обрабатываем движение
                time.sleep(self.config['loop_delay'])
        finally:
            # Отжимаем все кнопки мыши при завершении
            for action_key, button_info in self.config['mouse_button_actions'].items():
                if self.mouse_button_states[action_key]:
                    self.mouse_controller.release(button_info['button'])
            keyboard.unhook_all()
            print("Программа завершена.")

def setup_configuration():
    def perform_backspace():
        print("backspace (действие выполнено)")
        keyboard.press_and_release('backspace')

    def perform_enter():
        print("enter (действие выполнено)")
        keyboard.press_and_release('enter')

    def perform_scrollup():
        print("Скролл вверх (действие выполнено)")
        mouse.Controller().scroll(0, 5)
    
    def perform_scrolldown():
        print("Скролл вниз (действие выполнено)")
        mouse.Controller().scroll(0, -5)

    def perform_up():
        print("up (действие выполнено)")
        keyboard.press_and_release('up')

    def perform_down():
        print("down (действие выполнено)")
        keyboard.press_and_release('down')

    def perform_left():
        print("left (действие выполнено)")
        keyboard.press_and_release('left')

    def perform_right():
        print("right (действие выполнено)")
        keyboard.press_and_release('right')

    def perform_end():
        print("end (действие выполнено)")
        keyboard.press_and_release('end')

    config = {
        'activation_key': 'left ctrl',
        'activation_arrow_key': 'left alt',
        'turbo_key': 'space',
        'slow_key': 'left alt',
        'exit_key': 'home',
        'move_pixels': 5,
        'turbo_multiplier': 7,
        'slow_divisor': 2,
        'mouse_move_keys': {
            'i': (0, -1), 
            'k': (0, 1), 
            'j': (-1, 0), 
            'l': (1, 0),
        },
        # Кнопки мыши, которые можно зажимать/отжимать
        'mouse_button_actions': {
            ';': {'name': 'левая кнопка мыши', 'button': mouse.Button.left},
            "'": {'name': 'правая кнопка мыши', 'button': mouse.Button.right},
            'u': {'name': 'средняя кнопка мыши', 'button': mouse.Button.middle},
        },
        # Одноразовые действия (не кнопки мыши)
        'one_shot_actions': {
            'n': perform_scrollup,
            'm': perform_scrolldown,
            'h': perform_backspace,
            ".": perform_enter,
            "o": perform_end,
        },
        'one_shot_arrows': {
            'i': perform_up,
            'k': perform_down,
            'j': perform_left,
            "l": perform_right,
        },
        'loop_delay': 0.01 
    }
    return config

if __name__ == "__main__":
    try:
        configuration = setup_configuration()
        controller = MouseKeyController(configuration)
        controller.run()
    except Exception as e:
        print(f"\n[ОШИБКА]: {e}")
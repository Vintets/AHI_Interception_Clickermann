
__version_info__ = ('1', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'master by Vint'
__title__ = '--- AHI_Interception_Clickermann ---'
__copyright__ = 'Copyright 2024 (c)  bitbucket.org/Vintets'


from ctypes import windll, wintypes
from functools import partial
import os
import sys
import time
import tkinter as tk
from typing import Optional

from accessory import authorship
import interception
import win32api
import win32con
import win32gui


MSG_HOOK = {
    0xC430: 'wnd_show',
    0xC435: 'lclick',
    0xC436: 'rclick',
    0xC437: 'mclick',
    0xC438: 'mouse4click',
    0xC439: 'mouse5click',
    0xC43A: 'dblclick',

    0xC43B: 'ldown',
    0xC43C: 'lup',
    0xC43D: 'rdown',
    0xC43E: 'rup',
    0xC43F: 'mdown',
    0xC440: 'mup',
    0xC441: 'mouse4down',
    0xC442: 'mouse4up',
    0xC443: 'mouse5down',
    0xC444: 'mouse5up',

    0xC449: 'wheeldown',
    0xC44A: 'wheelup',

    0xC44B: 'move',
    0xC44C: 'mover',

    0xC450: 'keypress',
    0xC451: 'keypress_ex',
    0xC452: 'keydown',
    0xC454: 'keyup',
    0xC456: 'keystring',
}


def post_message_quit(hwnd_self: int) -> None:
    win32api.PostMessage(hwnd_self, win32con.WM_QUIT, 0, 0)


def post_message1(hwnd_self: int) -> None:
    # user32.PostMessageA(hwnd_self, 0x0400, 0, 0)
    win32gui.PostMessage(hwnd_self, 0x0400, 0, 0)
    print(f'send event to {hwnd_self}')  # noqa: T201


class ICP:
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        self.key_mapping = self._set_key_mapping()
        # interception.capture_keyboard()
        # interception.capture_mouse()
        interception.auto_capture_devices(keyboard=True, mouse=True)

    def _set_key_mapping(self) -> dict[str: int]:  # noqa: CFQ001
        key_mapping = {
            'f1': 0x70,
            'f2': 0x71,
            'f3': 0x72,
            'f4': 0x73,
            'f5': 0x74,
            'f6': 0x75,
            'f7': 0x76,
            'f8': 0x77,
            'f9': 0x78,
            'f10': 0x79,
            'f11': 0x7A,
            'f12': 0x7B,
            'f13': 0x7C,
            'f14': 0x7D,
            'f15': 0x7E,
            'f16': 0x7F,
            'f17': 0x80,
            'f18': 0x81,
            'f19': 0x82,
            'f20': 0x83,
            'f21': 0x84,
            'f22': 0x85,
            'f23': 0x86,
            'f24': 0x87,
            'backspace': 0x08,
            '\b': 0x08,  # same as backspace
            'tab': 0x09,
            '\t': 0x09,  # same as tab
            # 'super': 0x5B,
            'clear': 0x0C,
            'enter': 0x0D,
            '\n': 0x0D,  # same as enter key (newline)
            'return': 0x0D,
            'shift': 0x10,
            'ctrl': 0x11,
            'alt': 0x12,
            'pause': 0x13,
            'capslock': 0x14,
            'kana': 0x15,
            'hanguel': 0x15,
            'hangul': 0x15,
            'junja': 0x17,
            'final': 0x18,
            'hanja': 0x19,
            'kanji': 0x19,
            'esc': 0x1B,
            'escape': 0x1B,
            'convert': 0x1C,
            'nonconvert': 0x1D,
            'accept': 0x1E,
            'modechange': 0x1F,
            ' ': 0x20,
            'space': 0x20,
            'pgup': 0x21,
            'pgdn': 0x22,
            'pageup': 0x21,
            'pagedown': 0x22,
            'end': 0x23,
            'home': 0x24,
            'left': 0x25,
            'up': 0x26,
            'right': 0x27,
            'down': 0x28,
            'select': 0x29,
            'print': 0x2A,
            'execute': 0x2B,
            'prtsc': 0x2C,
            'prtscr': 0x2C,
            'prntscrn': 0x2C,
            'printscreen': 0x2C,
            'insert': 0x2D,
            'del': 0x2E,
            'delete': 0x2E,
            'help': 0x2F,
            'win': 0x5B,
            'winleft': 0x5B,
            'winright': 0x5C,
            'apps': 0x5D,
            'sleep': 0x5F,
            'num0': 0x60,
            'num1': 0x61,
            'num2': 0x62,
            'num3': 0x63,
            'num4': 0x64,
            'num5': 0x65,
            'num6': 0x66,
            'num7': 0x67,
            'num8': 0x68,
            'num9': 0x69,
            'multiply': 0x6A,
            '*': 0x6A,
            'add': 0x6B,
            'plus': 0x6B,
            '+': 0x6B,
            'separator': 0x6C,
            'subtract': 0x6D,
            'minus': 0x6D,
            'dash': 0x6D,
            'decimal': 0x6E,
            'divide': 0x6F,
            'numlock': 0x90,
            'scrolllock': 0x91,
            'shiftleft': 0xA0,
            'shiftright': 0xA1,
            'ctrlleft': 0xA2,
            'ctrlright': 0xA3,
            'altleft': 0xA4,
            'altright': 0xA5,
            'browserback': 0xA6,
            'browserforward': 0xA7,
            'browserrefresh': 0xA8,
            'browserstop': 0xA9,
            'browsersearch': 0xAA,
            'browserfavorites': 0xAB,
            'browserhome': 0xAC,
            'volumemute': 0xAD,
            'volumedown': 0xAE,
            'volumeup': 0xAF,
            'nexttrack': 0xB0,
            'prevtrack': 0xB1,
            'stop': 0xB2,
            'playpause': 0xB3,
            'launchmail': 0xB4,
            'launchmediaselect': 0xB5,
            'launchapp1': 0xB6,
            'launchapp2': 0xB7,
        }

        for cod in range(32, 128):
            key_mapping[chr(cod).lower()] = windll.user32.VkKeyScanA(wintypes.WCHAR(chr(cod)))

        # for k, v in key_mapping.items():
        #     map_virtual_key = windll.user32.MapVirtualKeyA(divmod(v, 0x100)[1], 0)
        #     print(f'{k:<19}{v:<5}{map_virtual_key:<3}')
        return key_mapping

    def get_char_by_keycode(self, keycode) -> Optional[str]:
        try:
            return list(self.key_mapping.keys())[list(self.key_mapping.values()).index(keycode)]
        except ValueError:
            return None

    def move(self, _x: Optional[int] = None, _y: Optional[int] = None) -> None:
        interception.move_to(_x, _y)

    def move_relative(self, _x: Optional[int] = None, _y: Optional[int] = None) -> None:
        interception.move_relative(_x, _y)

    def click(self,
              _x: Optional[int] = None,
              _y: Optional[int] = None,
              button: str = 'left',
              clicks: int = 1,
              interval: int | float = 0.1,
              delay: int | float = 0,
              ) -> None:
        """Presses a mouse button.

        Parameters
        ----------
        button :class:`str`: 'left', 'right', 'middle', 'mouse4', 'mouse5'
            The button to click once moved to the location (if passed), default "left".

        clicks :class:`int`:
            The amount of mouse clicks to perform with the given button, default 1.

        interval :class:`int | float`:
            The interval between multiple clicks, only applies if clicks > 1, default 0.1.

        delay :class:`int | float`:
            The delay between moving and clicking, default 0 (0.3).
        """
        interception.click(_x, _y, button=button, clicks=clicks, interval=interval, delay=delay)
        if self.debug:
            print(f'{button} Mouse Button clicked ({_x}, {_y})')  # noqa: T201

    def mouse_down(self,
                   _x: Optional[int] = None,
                   _y: Optional[int] = None,
                   button: str = 'left',
                   delay: int | float = 0,
                   ) -> None:
        if _x is not None:
            interception.move_to(_x, _y)
            time.sleep(delay)

        interception.mouse_down(button)

    def mouse_up(self,
                 _x: Optional[int] = None,
                 _y: Optional[int] = None,
                 button: str = 'left',
                 delay: int | float = 0,
                 ) -> None:
        if _x is not None:
            interception.move_to(_x, _y)
            time.sleep(delay)

        interception.mouse_up(button)

    def wheeldown(self, mult: Optional[int] = 1):
        for _ in range(mult):
            interception.scroll(direction='down')

    def wheelup(self, mult: Optional[int] = 1):
        for _ in range(mult):
            interception.scroll(direction='up')

    def keypress(self, key: str | int, presses: int = 1, interval_ms: int = 0, modif_key=None) -> None:
        if isinstance(key, int):
            print(f'lparam {key}')
            key = self.get_char_by_keycode(key)
        if key is None:
            return
        print(f'{key = }')
        interval = interval_ms / 1000
        if modif_key is not None:
            with interception.hold_key(modif_key):
                interception.press(key, presses=presses, interval=interval)
        else:
            interception.press(key, presses=presses, interval=interval)

    def keystring(self, term: str, interval_ms: int = 0) -> None:
        interval = interval_ms / 1000
        interception.write(term, interval=interval)

    def keydown(self, key: str, delay: Optional[float | int] = 0) -> None:
        interception.key_down(key, delay=delay)
        # UnknownKeyError

    def keyup(self, key: str, delay: Optional[float | int] = 0) -> None:
        interception.key_up(key, delay=delay)


class MainWin(tk.Tk):
    def __init__(self, msg_hook: dict, wnd_title: str, debug: bool = False, **kwargs) -> None:
        self.debug = debug
        self.icp = ICP(debug=debug)
        self.msg_hook = msg_hook
        tk.Tk.__init__(self, **kwargs)
        self.title(wnd_title)
        self.geometry('120x80+10+10')
        # store everything in a frame
        # self.container = tk.Frame(self)
        # self.container.pack(side='top', fill='both', expand=True)

        print(f'{self.winfo_id() = }')  # noqa: T201, E251, E202
        self.hwnd = int(self.frame(), 16)
        print(f'{self.hwnd = }  {self.frame()}')  # noqa: T201, E251, E202
        bt1 = tk.Button(self, text='PostMessage 1', command=lambda: post_message1(self.hwnd))  # callback=lambda x=x: f(x)
        bt1.pack()
        bt2 = tk.Button(self, text='Скрыть окно', command=self.withdraw)
        bt2.pack()
        # bt3 = tk.Button(self, text='Тест', command=self.test_command)
        # bt3.pack()
        bt5 = tk.Button(self, text='Выход', command=exit_from_program)
        bt5.pack()
        self.update()
        # self.tick()
        pass

    def tick(self) -> None:
        self.after(20, self.tick)  # <----------- this is the method you are looking for
        code, msg = win32gui.GetMessage(0, 0, 0)
        # print(code, msg)
        if code < 0:
            error = win32api.GetLastError()
            raise RuntimeError(error)
        self.handler(msg)
        win32gui.TranslateMessage(msg)
        win32gui.DispatchMessage(msg)

    def handler(self, msg: tuple) -> None:
        hwnd_e, msgid, wparam, lparam, time_, point = msg
        if hwnd_e != self.hwnd:
            return
        if self.debug:
            print(msg)  # noqa: T201
        match self.msg_hook.get(msgid):
            case 'wnd_show':
                self.deiconify()
            case 'lclick':
                self.icp.click(*self.unpuck(lparam), button='left')
            case 'rclick':
                self.icp.click(*self.unpuck(lparam), button='right')
            case 'mclick':
                self.icp.click(*self.unpuck(lparam), button='middle')
            case 'mouse4click':
                self.icp.click(*self.unpuck(lparam), button='mouse4')
            case 'mouse5click':
                self.icp.click(*self.unpuck(lparam), button='mouse5')
            case 'dblclick':
                self.icp.click(*self.unpuck(lparam), button='left', clicks=2)
            case 'ldown':
                self.icp.mouse_down(*self.unpuck(lparam), button='left')
            case 'lup':
                self.icp.mouse_up(*self.unpuck(lparam), button='left')
            case 'rdown':
                self.icp.mouse_down(*self.unpuck(lparam), button='right')
            case 'rup':
                self.icp.mouse_up(*self.unpuck(lparam), button='right')
            case 'mdown':
                self.icp.mouse_down(*self.unpuck(lparam), button='middle')
            case 'mup':
                self.icp.mouse_up(*self.unpuck(lparam), button='middle')
            case 'mouse4down':
                self.icp.mouse_down(*self.unpuck(lparam), button='mouse4')
            case 'mouse4up':
                self.icp.mouse_up(*self.unpuck(lparam), button='mouse4')
            case 'mouse5down':
                self.icp.mouse_down(*self.unpuck(lparam), button='mouse5')
            case 'mouse5up':
                self.icp.mouse_up(*self.unpuck(lparam), button='mouse5')
            case 'wheeldown':
                self.icp.wheeldown(mult=lparam)
            case 'wheelup':
                self.icp.wheelup(mult=lparam)
            case 'move':
                self.icp.move(*self.unpuck(lparam))
            case 'mover':
                self.icp.move_relative(*self.unpuck(lparam))
            case 'keypress':
                self.icp.keypress(lparam)
            case 'keypress_ex':
                self.icp.keypress(lparam, interval_ms=wparam)
            case 'keydown':
                self.icp.keydown(lparam)
            case 'keyup':
                self.icp.keyup(lparam)
            # case 'keystring':
            #     self.icp.keystring()
            case _:
                if self.debug:
                    print('Неизвестная команда')  # noqa: T201

    def unpuck(self, lparam: int) -> tuple[int, int]:
        _x = win32api.LOWORD(lparam)
        _y = win32api.HIWORD(lparam)
        return _x, _y

    def test_command(self) -> None:
        self.icp.click(*(200, 300), button='left')


def exit_from_program(code: int = 0) -> None:
    try:
        sys.exit(code)
    except SystemExit:
        os._exit(code)


def validate_transferred_argument() -> tuple[str, int]:
    try:
        wnd_title = sys.argv[1]
        hwnd_cm = int(sys.argv[2])
    except (IndexError, ValueError):
        print('Не переданы правильные параметры запуска')  # noqa: T201
        exit_from_program(code=1)
    return wnd_title, hwnd_cm


def post_message(wParam: int, lParam: int, hwnd: int) -> None:  # noqa: N803
    win32api.PostMessage(hwnd, 1024, wParam, lParam)


def main(test: bool = False, debug: bool = False) -> None:
    if not test:
        wnd_title, hwnd_cm = validate_transferred_argument()
    else:
        wnd_title = 'tktest'
        hwnd_cm = 7736026
    print(f'{wnd_title = }  {hwnd_cm = }')  # noqa: T201, E251, E202

    app = MainWin(MSG_HOOK, wnd_title, debug=debug)

    # отправляем clickermann-у свой hwnd
    post_message_cm = partial(post_message, hwnd=hwnd_cm)
    post_message_cm(app.hwnd, 0)

    app.tick()
    app.mainloop()


if __name__ == '__main__':
    _width = 130
    _hight = 50
    if sys.platform == 'win32':
        os.system('color 71')
        # os.system('mode con cols=%d lines=%d' % (_width, _hight))

    authorship(__author__, __title__, __version__, __copyright__)  # width=_width

    # print(interception.KEYBOARD_MAPPING)
    # print(ICP().key_mapping)
    # ICP().key_mapping
    # exit()
    try:
        main(test=False, debug=True)
    except KeyboardInterrupt:
        print('Работа программы прервана пользователем')  # noqa: T201
        exit_from_program()

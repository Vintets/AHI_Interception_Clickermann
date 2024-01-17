
__version_info__ = ('1', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'master by Vint'
__title__ = '--- AHI_Interception_Clickermann ---'
__copyright__ = 'Copyright 2024 (c)  bitbucket.org/Vintets'


from functools import partial
import os
import sys
import time
import tkinter as tk
from typing import Optional

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
        # interception.capture_keyboard()
        # interception.capture_mouse()
        interception.auto_capture_devices(keyboard=True, mouse=True)

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

    def keypress(self, key: str, presses: int = 1, interval: int | float = 0.1, modif_key=None) -> None:
        if modif_key is not None:
            with interception.hold_key(modif_key):
                interception.press(key, presses=presses, interval=interval)
        else:
            interception.press(key, presses=presses, interval=interval)


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
        os.system('mode con cols=%d lines=%d' % (_width, _hight))
    else:
        os.system('setterm -background white -foreground white -store')
        # ubuntu terminal
        os.system('setterm -term linux -back $blue -fore white -clear')

    try:
        main(test=False, debug=True)
    except KeyboardInterrupt:
        print('Работа программы прервана пользователем')  # noqa: T201
        exit_from_program()

import os
import sys
import time
from functools import partial
from typing import Optional
import tkinter as tk
import win32api
import win32gui
import win32con
import interception


MSG_HOOK ={
    'wnd_show': 0xC430,
    'lclick': 0xC435,
    'rclick': 0xC436,
    'mclick': 0xC437,
    'mouse4click': 0xC438,
    'mouse5click': 0xC439,
    'dblclick': 0xC43A,

    'ldown': 0xC43B,
    'lup': 0xC43C,
    'rdown': 0xC43D,
    'rup': 0xC43E,
    'mdown': 0xC43F,
    'mup': 0xC440,
}


def post_message_quit(hwnd_self):
    win32api.PostMessage(hwnd_self, win32con.WM_QUIT, 0, 0)


def post_message1(hwnd_self):
    # user32.PostMessageA(hwnd_self, 0x0400, 0, 0)
    win32gui.PostMessage(hwnd_self, 0x0400, 0, 0)
    print(f'send event to {hwnd_self}')


class ICP:
    def __init__(self):
        # interception.capture_keyboard()
        # interception.capture_mouse()
        interception.auto_capture_devices(keyboard=True, mouse=True)

    def move(self, x, y):
        interception.move_to(x, y)

    def move_relative(self, x, y):
        interception.move_relative(x, y)

    def click(self,
              x: Optional[int] = None,
              y: Optional[int] = None,
              button: str = 'left',
              clicks: int = 1,
              interval: int | float = 0.1,
              delay: int | float = 0,
              ):
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
        interception.click(x, y, button=button, clicks=clicks, interval=interval, delay=delay)
        print(f'{button} Mouse Button clicked ({x}, {y})')

    def mouse_down(self,
              x: Optional[int] = None,
              y: Optional[int] = None,
              button: str = 'left',
              delay: int | float = 0,
              ):
        if x is not None:
            interception.move_to(x, y)
            time.sleep(delay)

        interception.mouse_down(button)

    def mouse_up(self,
              x: Optional[int] = None,
              y: Optional[int] = None,
              button: str = 'left',
              delay: int | float = 0,
              ):
        if x is not None:
            interception.move_to(x, y)
            time.sleep(delay)

        interception.mouse_up(button)

    def keypress(self, key: str, presses: int = 1, interval: int | float = 0.1, modif_key=None):
        if modif_key is not None:
            with interception.hold_key(modif_key):
                interception.press(key, presses=presses, interval=interval)
        else:
            interception.press(key, presses=presses, interval=interval)


class MainWin(tk.Tk):
    def __init__(self, msg_hook, wnd_title, *args, **kwargs):
        self.icp = ICP()
        self.msg_hook = msg_hook
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(wnd_title)
        self.geometry('120x80+10+10')
        # store everything in a frame
        # self.container = tk.Frame(self)
        # self.container.pack(side='top', fill='both', expand=True)

        print(f'{self.winfo_id() = }')
        self.hwnd = int(self.frame(), 16)
        print(f'{self.hwnd = }  {self.frame()}')
        bt1 = tk.Button(self, text='PostMessage 1', command=lambda: post_message1(self.hwnd)) # callback=lambda x=x: f(x)
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

    def tick(self):
        self.after(20, self.tick)  # <----------- this is the method you are looking for
        code, msg = win32gui.GetMessage(0, 0, 0)
        # print(code, msg)
        if code < 0:
            error = win32api.GetLastError()
            raise RuntimeError(error)
        self.handler(msg)
        win32gui.TranslateMessage(msg)
        win32gui.DispatchMessage(msg)

    def handler(self, msg):
        hwnd_e, msgid, wparam, lparam, time_, point = msg
        if hwnd_e != self.hwnd:
            return
        print(msg)
        if msgid == self.msg_hook.get('wnd_show'):
            self.deiconify()
        elif msgid == self.msg_hook.get('lclick'):
            self.icp.click(*self.unpuck(lparam), button='left')
        elif msgid == self.msg_hook.get('rclick'):
            self.icp.click(*self.unpuck(lparam), button='right')
        elif msgid == self.msg_hook.get('mclick'):
            self.icp.click(*self.unpuck(lparam), button='middle')
        elif msgid == self.msg_hook.get('mouse4click'):
            self.icp.click(*self.unpuck(lparam), button='mouse4')
        elif msgid == self.msg_hook.get('mouse5click'):
            self.icp.click(*self.unpuck(lparam), button='mouse5')
        elif msgid == self.msg_hook.get('dblclick'):
            self.icp.click(*self.unpuck(lparam), button='left', clicks=2)
        elif msgid == self.msg_hook.get('ldown'):
            self.icp.mouse_down(*self.unpuck(lparam), button='left')
        elif msgid == self.msg_hook.get('lup'):
            self.icp.mouse_up(*self.unpuck(lparam), button='left')
        elif msgid == self.msg_hook.get('rdown'):
            self.icp.mouse_down(*self.unpuck(lparam), button='right')
        elif msgid == self.msg_hook.get('rup'):
            self.icp.mouse_up(*self.unpuck(lparam), button='right')
        elif msgid == self.msg_hook.get('mdown'):
            self.icp.mouse_down(*self.unpuck(lparam), button='middle')
        elif msgid == self.msg_hook.get('mup'):
            self.icp.mouse_up(*self.unpuck(lparam), button='middle')

    def unpuck(self, lparam):
        x = win32api.LOWORD(lparam)
        y = win32api.HIWORD(lparam)
        return x,y

    def test_command(self):
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
        print('Не переданы правильные параметры запуска')
        exit_from_program(code=1)
    return wnd_title, hwnd_cm


def post_message(wParam, lParam, hwnd):
    win32api.PostMessage(hwnd, 1024, wParam, lParam)


def main(test=False):
    if not test:
        wnd_title, hwnd_cm = validate_transferred_argument()
    else:
        wnd_title = 'tktest'
        hwnd_cm = 7736026
    print(f'{wnd_title = }  {hwnd_cm = }')

    app = MainWin(MSG_HOOK, wnd_title)

    # отправляем clickermann-у свой hwnd
    post_message_CM = partial(post_message, hwnd=hwnd_cm)
    post_message_CM(app.hwnd, 0)

    app.tick()
    app.mainloop()


if __name__ == "__main__":
    try:
        main(test=False)
    except KeyboardInterrupt:
        print('Работа программы прервана пользователем')
        exit_from_program()

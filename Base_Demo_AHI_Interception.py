import interception
import time


# interception.capture_keyboard()
# interception.capture_mouse()

interception.auto_capture_devices(keyboard=True, mouse=True)


interception.move_to(960, 540)

with interception.hold_key('shift'):
    interception.press('a')

# interception.click(120, 160, button='right', delay=1)


interception.click(2480, 420, button='left', delay=1)
time.sleep(1)

interception.press('up')

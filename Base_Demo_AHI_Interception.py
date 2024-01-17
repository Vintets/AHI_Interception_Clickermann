import interception


# interception.capture_keyboard()
# interception.capture_mouse()

interception.auto_capture_devices(keyboard=True, mouse=True)


interception.move_to(960, 540)

with interception.hold_key('shift'):
    interception.press('a')

interception.click(120, 160, button='right', delay=1)


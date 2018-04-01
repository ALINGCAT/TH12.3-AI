# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 09:27:39 2018

@author: 北海若
"""

import win32gui
import win32con
from PIL import ImageGrab
import time
import ctypes


# from: https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


hwnd = win32gui.FindWindow("th123_110", "东方非想天则 ～ 追寻特大型人偶之谜 Ver1.10(beta)")
if not hwnd:
    print('window not found!')
else:
    print(hwnd)


def press_key(code):
    for c in code:
        if type(c) == list:
            for cc in c:
                PressKey(cc)
            time.sleep(0.03)
            for cc in c:
                ReleaseKey(cc)
        else:
            PressKey(c)
            time.sleep(0.03)
            ReleaseKey(c)
        time.sleep(0.03)
        print(c)


def conv_keycode(action):
    if action == "2":
        return [0x1F]
    elif action == "8":
        return [0x11]
    elif action == "4":
        return [0x1E]
    elif action == "6":
        return [0x20]
    elif action == "3":
        return [0x1F, 0x20]
    elif action == "1":
        return [0x1F, 0x1E]
    elif action == "9":
        return [0x11, 0x20]
    elif action == "7":
        return [0x11, 0x1E]
    elif action == "A":
        return [0x24]
    elif action == "B":
        return [0x25]
    elif action == "C":
        return [0x26]
    elif len(action) == 2 and (action[1] == "A" or action[1] == "B" or action[1] == "C"):
        return [conv_keycode(action[0])[0], conv_keycode(action[1])[0]]
    last_order_list = []
    for x in action:
        last_order_list.append(conv_keycode(x))
    return last_order_list


def fetch_screen():
    game_rect = win32gui.GetWindowRect(hwnd)
    src_image = ImageGrab.grab(game_rect)
    src_image.show()

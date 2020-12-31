# BYTE      = c_ubyte
# WORD      = c_ushort
# DWORD     = c_ulong
# LPBYTE    = POINTER(c_ubyte)
# LPTSTR    = POINTER(c_char)
# HANDLE    = c_void_p
# PVOID     = c_void_p
# LPVOID    = c_void_p
# UNIT_PTR  = c_ulong
# SIZE_T    = c_ulong

from pyWinhook import HookManager
import pythoncom

import ctypes
import ctypes.wintypes
import sys

from helper import *


PROCESS_ALL_ACCESS = 0x1F0FFF
GODMODE_BASE = 0x881548
NOCLIP_BASE = 0xA18D54
NORELOAD_BASE = 0xF42F10


def toggleByte(processHandle, base):
    buffer = ctypes.create_string_buffer(1)
    ctypes.windll.kernel32.ReadProcessMemory(
        processHandle, base, buffer, ctypes.sizeof(buffer), None)

    current_value = buffer.value.decode()

    if not current_value:
        current_value = 0
    else:
        current_value = 1

    buffer = ctypes.c_char_p(chr(current_value ^ 1).encode())
    ctypes.windll.kernel32.WriteProcessMemory(
        processHandle, base, buffer, ctypes.sizeof(ctypes.c_byte), None)


def cheatDispatcher(event):
    # F1..F12 -> 112..123
    ch = event.KeyID

    if ch == 123:
        ctypes.windll.kernel32.CloseHandle(processHandle)
        hm.UnhookKeyboard()
        sys.exit()

    if ch == 122:
        toggleByte(processHandle, base + GODMODE_BASE)

    if ch == 121:
        toggleByte(processHandle, base + NOCLIP_BASE)

    if ch == 120:
        toggleByte(processHandle, base + NORELOAD_BASE)

    return True


if not isAdmin():
    print("[!] Please run the program as an administrator!")
    sys.exit()


pid = None if len(sys.argv) < 2 else int(sys.argv[1])
executableName = None if len(sys.argv) < 3 else sys.argv[2]

if not pid:
    print(f"[!] PID not provided! Trying to get it automatically... Looking for 'Call of Duty 4' title.")
    pid = getPid()
    if not pid:
        print(f"[!] Was not able to get PID.")
        print(f"[!] Run : {sys.argv[0]} [PID] [EXEC_NAME/'iw3sp.exe']")
        sys.exit(-1)

    print(f"[+] Got PID - {pid}")

processHandle = ctypes.windll.kernel32.OpenProcess(
    PROCESS_ALL_ACCESS, False, pid)
base, moduleName = getBaseAddress(
    pid, processHandle, executableName=executableName)

print(f"[+] Base address for {moduleName} is {hex(base)}.")
hm = HookManager()
hm.KeyDown = cheatDispatcher
hm.HookKeyboard()
print("[+] Hooked to keyboard successfully!")
pythoncom.PumpMessages()

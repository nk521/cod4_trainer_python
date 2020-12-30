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


PROCESS_ALL_ACCESS = 0x1F0FFF
GODMODE_BASE = 0x881548
NOCLIP_BASE = 0xA18D54
NORELOAD_BASE = 0xF42F10

# this is to check if current user is an admin or not
# https://stackoverflow.com/a/15774626


def isAdmin():
    class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
        _fields_ = [
            ("byte0", ctypes.c_byte),
            ("byte1", ctypes.c_byte),
            ("byte2", ctypes.c_byte),
            ("byte3", ctypes.c_byte),
            ("byte4", ctypes.c_byte),
            ("byte5", ctypes.c_byte),
        ]

    nt_authority = SID_IDENTIFIER_AUTHORITY()
    nt_authority.byte5 = 5

    SECURITY_BUILTIN_DOMAIN_RID = 0x20
    DOMAIN_ALIAS_RID_ADMINS = 0x220
    administrators_group = ctypes.c_void_p()
    if ctypes.windll.advapi32.AllocateAndInitializeSid(ctypes.byref(nt_authority), 2, SECURITY_BUILTIN_DOMAIN_RID, DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, ctypes.byref(administrators_group)) == 0:
        raise Exception("AllocateAndInitializeSid failed")

    try:
        is_admin_ = ctypes.wintypes.BOOL()
        if ctypes.windll.advapi32.CheckTokenMembership(0, administrators_group, ctypes.byref(is_admin_)) == 0:
            raise Exception("CheckTokenMembership failed")
        is_admin = is_admin_.value != 0
        return is_admin

    finally:
        ctypes.windll.advapi32.FreeSid(administrators_group)


def getBaseAddress(pid, processHandle, executableName=None):
    class MODULEINFO(ctypes.Structure):
        _fields_ = [
            ("baseOfDll", ctypes.c_void_p),
            ("sizeOfImage", ctypes.c_ulong),
            ("entryPoint", ctypes.c_void_p),
        ]

    # sometimes currModule is just empty
    # this is why I included a fix executable name
    if not executableName:
        currModule = ctypes.create_string_buffer(2048)
        currModuleCount = ctypes.c_ulong(ctypes.sizeof(currModule))
        ctypes.windll.psapi.GetProcessImageFileNameA(
            processHandle, ctypes.byref(currModule), ctypes.byref(currModuleCount))

        if not currModule.value:
            print("[!] Restart the program!")
            sys.exit(-1)

    hModulesArray = (ctypes.c_void_p * 1024)()
    cbNeeded = ctypes.c_ulong()
    ctypes.windll.psapi.EnumProcessModules(
        processHandle, hModulesArray, ctypes.sizeof(hModulesArray), ctypes.byref(cbNeeded))

    for hModule_ in hModulesArray:
        if not None:
            try:
                cPath = ctypes.create_string_buffer(1024)
                ctypes.windll.psapi.GetModuleFileNameExA(
                    processHandle, hModule_, cPath, ctypes.c_ulong(1024))

                if not executableName:
                    if currModule.value.decode().split("\\")[-1] == cPath.value.decode().split("\\")[-1]:
                        hModule = hModule_
                        break
                else:
                    if executableName.lower() == cPath.value.decode().split("\\")[-1].lower():
                        hModule = hModule_
                        break
            except:
                pass

    moduleInfoObject = MODULEINFO()
    ctypes.windll.psapi.GetModuleInformation(processHandle, hModule, ctypes.byref(
        moduleInfoObject), ctypes.sizeof(MODULEINFO))

    base = moduleInfoObject.baseOfDll
    return base, executableName if executableName else currModule.value.decode().split("\\")[-1]


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
    print("Please run the program as an administrator!")
    sys.exit()


pid = int(sys.argv[1])
executableName = None if len(sys.argv) < 3 else sys.argv[2]

processHandle = ctypes.windll.kernel32.OpenProcess(
    PROCESS_ALL_ACCESS, False, pid)
base, moduleName = getBaseAddress(
    pid, processHandle, executableName=executableName)

hm = HookManager()
hm.KeyDown = cheatDispatcher
hm.HookKeyboard()
pythoncom.PumpMessages()

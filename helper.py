import ctypes
import ctypes.wintypes
import sys
import win32con

from structures import MODULEINFO, SID_IDENTIFIER_AUTHORITY

def getWindow(title="Call of Duty 4"):
    titleChar = ctypes.c_char_p(title.encode())
    window = ctypes.windll.user32.FindWindowA(0, titleChar)
    return window

def getPid():
    window = getWindow()
    pid = ctypes.c_int(0)
    ctypes.windll.user32.GetWindowThreadProcessId(window, ctypes.byref(pid))
    
    return pid.value


# this is to check if current user is an admin or not
# https://stackoverflow.com/a/15774626
def isAdmin():
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
    return base, executableName if executableName else currModule.value.decode().split("\\")[-1], hModule


def isDWMCompositionEnabled():
    enabled = ctypes.c_bool(0)
    ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(enabled))
    if not enabled:
        print("[!] Please enable Windows Aero!")
        return False
    return True

# def MAKEINTRESOURCEA(i):
#     cast1 = ctypes.cast((ctypes.c_int*1)(i), ctypes.POINTER(ctypes.c_ushort)).contents
#     cast2 = ctypes.cast((ctypes.c_ushort*1)(cast1), ctypes.POINTER(ctypes.c_ulong)).contents
#     cast3 = ctypes.cast((ctypes.c_ulong*1)(cast2), ctypes.POINTER(ctypes.c_char_p)).contents
#     return cast3


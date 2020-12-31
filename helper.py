import ctypes
import ctypes.wintypes
import sys


def getPid(title="Call of Duty 4"):
    title_char = ctypes.c_char_p(title.encode())
    window = ctypes.windll.user32.FindWindowA(0, title_char)
    pid = ctypes.c_int(0)
    ctypes.windll.user32.GetWindowThreadProcessId(window, ctypes.byref(pid))

    return pid.value


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
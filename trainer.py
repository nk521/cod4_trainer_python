import ctypes
import ctypes.wintypes
import sys

PROCESS_ALL_ACCESS = 0x1F0FFF

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

if not isAdmin():
    print("Please run the program as an administrator!")
    sys.exit()

pid = int(sys.argv[1])
processHandle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

address = 0x00000
buffer = ctypes.c_buffer(4)

if ctypes.windll.kernel32.ReadProcessMemory(processHandle, address, buffer, ctypes.sizeof(buffer), None):
    print(ord(buffer.value.decode()))

else:
    print("something fucked up")

buffer = ctypes.c_char_p(chr(10).encode())
a = ctypes.windll.kernel32.WriteProcessMemory(processHandle, address, buffer, ctypes.sizeof(ctypes.c_byte), None)
print(a)

ctypes.windll.kernel32.CloseHandle(processHandle)

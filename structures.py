import ctypes
import ctypes.wintypes
import d3d

WNDPROCTYPE = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.wintypes.HWND, ctypes.c_uint, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)


class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
    _fields_ = [
        ("byte0", ctypes.c_byte),
        ("byte1", ctypes.c_byte),
        ("byte2", ctypes.c_byte),
        ("byte3", ctypes.c_byte),
        ("byte4", ctypes.c_byte),
        ("byte5", ctypes.c_byte),
    ]


class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("baseOfDll", ctypes.c_void_p),
        ("sizeOfImage", ctypes.c_ulong),
        ("entryPoint", ctypes.c_void_p),
    ]


class WNDCLASSEX(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("style", ctypes.c_uint),
        ("lpfnWndProc", WNDPROCTYPE),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", ctypes.wintypes.HINSTANCE),
        ("hIcon", ctypes.wintypes.HICON),
        ("hCursor", ctypes.wintypes.HANDLE),
        ("hbrBackground", ctypes.wintypes.HBRUSH),
        ("lpszMenuName", ctypes.wintypes.LPCWSTR),
        ("lpszClassName", ctypes.wintypes.LPCWSTR),
        ("hIconSm", ctypes.wintypes.HICON)
    ]


class MARGINS(ctypes.Structure):
  _fields_ = [
        ("cxLeftWidth", ctypes.c_int),
        ("cxRightWidth", ctypes.c_int),
        ("cyTopHeight", ctypes.c_int),
        ("cyBottomHeight", ctypes.c_int)
    ]


class OVERLAY(ctypes.Structure):
    # copied from guided hacking forum
    # dont remember the exact link
    _fields_ = [
        ("Class", WNDCLASSEX),
        ("Name", ctypes.c_char * 256),
        ("Width", ctypes.c_int),
        ("Height", ctypes.c_int),
        ("Window", ctypes.wintypes.HWND),
        ("Message", ctypes.wintypes.MSG),
        ("Margin", MARGINS),
    ]

# class D3DPRESENT_PARAMETERS(ctypes.Structure):
#     _fields_ = (
#         ('BackBufferWidth', ctypes.c_uint),
#         ('BackBufferHeight', ctypes.c_uint),
#         ('BackBufferFormat', ctypes.c_uint),
#         ('BackBufferCount', ctypes.c_uint),
#         ('MultiSampleType', ctypes.c_uint),
#         ('MultiSampleQuality', ctypes.c_ulong),
#         ('SwapEffect', ctypes.c_uint),
#         ('hDeviceWindow', ctypes.wintypes.HWND),
#         ('Windowed', ctypes.c_bool),
#         ('EnableAutoDepthStencil', ctypes.c_bool),
#         ('AutoDepthStencilFormat', ctypes.c_uint),
#         ('Flags', ctypes.c_ulong),
#         ('FullScreen_RefreshRateInHz', ctypes.c_uint),
#         ('PresentationInterval', ctypes.c_uint)
#     )


# class DIRECTX(ctypes.Structure):
#     _fields_ = [
#         ("Object", ctypes.POINTER(d3d.IDirect3D9Ex)),
#         ("Device", ctypes.POINTER(d3d.IDirect3DDevice9Ex)),
#         ("Param", d3d.D3DPRESENT_PARAMETERS),
#         ("Font", ctypes.POINTER(ctypes.c_ulong)),
#         ("espFont", ctypes.POINTER(ctypes.c_ulong)),
#         ("FontWarning", ctypes.POINTER(ctypes.c_ulong)),
#         ("Line", ctypes.POINTER(ctypes.c_ulong)),
#     ]

class DIRECTX(ctypes.Structure):
    _fields_ = [
        ("Object", ctypes.c_void_p),
        ("Device", ctypes.c_void_p),
        # ("Param", d3d.D3DPRESENT_PARAMETERS),
        ("Font", ctypes.c_void_p),
        ("espFont", ctypes.c_void_p),
        # ("FontWarning", ctypes.POINTER(ctypes.c_ulong)),
        # ("Line", ctypes.POINTER(ctypes.c_ulong)),
    ]


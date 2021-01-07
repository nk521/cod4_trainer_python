import helper
import structures

import ctypes
import ctypes.wintypes
import sys
import win32con
import winerror

import d3d

D3D_SDK_VERSION  = 31 | 0x80000000

D3DFMT_A8R8G8B8 = 21
D3DPOOL_SYSTEMMEM = 2
		
D3DADAPTER_DEFAULT = 0
D3DSWAPEFFECT_DISCARD = 1
D3DDEVTYPE_HAL = 1
D3DCREATE_SOFTWARE_VERTEXPROCESSING = 0x00000020

D3DFMT_D16 = 80
D3DMULTISAMPLE_NONE = 0

def overlayCreateClass(winProc, windowName, hModule, overlayObj):
    overlayObj.Name = windowName.encode()
    overlayObj.Class.cbClsExtra = 0
    overlayObj.Class.cbSize = ctypes.sizeof(structures.WNDCLASSEX)
    overlayObj.Class.cbWndExtra = 0
    overlayObj.Class.hbrBackground = ctypes.windll.gdi32.CreateSolidBrush(ctypes.wintypes.RGB(0, 0, 0))
    overlayObj.Class.hCursor = ctypes.windll.user32.LoadCursorA(0, win32con.IDC_ARROW)
    overlayObj.Class.hIcon = ctypes.windll.user32.LoadIconA(0, win32con.IDI_APPLICATION)
    overlayObj.Class.hIconSm = ctypes.windll.user32.LoadIconA(0, win32con.IDI_APPLICATION)
    overlayObj.Class.hInstance = hModule
    overlayObj.Class.lpfnWndProc = winProc
    overlayObj.Class.lpszClassName = overlayObj.Name.decode()
    overlayObj.Class.lpszMenuName = overlayObj.Name.decode()
    overlayObj.Class.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW

    if not ctypes.windll.user32.RegisterClassExA(ctypes.byref(overlayObj.Class)):
        return False
    
    return True



def overlayInit(overlayObj):
    window = helper.getWindow()
    size = ctypes.wintypes.RECT()

    ctypes.windll.user32.GetWindowRect(window, ctypes.byref(size))
    overlayObj.Width = size.right - size.left
    overlayObj.Height = size.bottom - size.top

    style = ctypes.windll.user32.GetWindowLongA(window, win32con.GWL_STYLE)

    if (style & win32con.WS_BORDER):
        size.top += 23
        overlayObj.Height -= 23
    
    ctypes.windll.user32.MoveWindow(overlayObj.Window, size.left, size.top, overlayObj.Width, overlayObj.Height, True)
    
    overlayObj.Margin.cxLeftWidth = 0
    overlayObj.Margin.cxRightWidth = 0
    overlayObj.Margin.cyTopHeight = overlayObj.Width
    overlayObj.Margin.cyBottomHeight = overlayObj.Height

    return True


def overlayCreateWindow(overlayObj, hModule):
    overlayObj.Window = ctypes.windll.user32.CreateWindowExA(win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT, overlayObj.Name.decode(), overlayObj.Name.decode(), win32con.WS_POPUP, 1, 1, overlayObj.Width, overlayObj.Height, 0, 0, hModule, 0)
    if overlayObj.Window:
        ctypes.windll.user32.SetLayeredWindowAttributes(overlayObj.Window, ctypes.wintypes.RGB(0,0,0), 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        ctypes.windll.user32.ShowWindow(overlayObj.Window, win32con.SW_SHOW)
        ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(overlayObj.Window, ctypes.byref(overlayObj.Margin))

        return True
    
    else:
        return False


def directxInit(overlayObj, directxObj):
    helperModule = ctypes.WinDLL("./classlink.dll")
    directxObj.Device = helperModule.directxInit(overlayObj.Window, overlayObj.Width, overlayObj.Height)
    return directxObj.Device

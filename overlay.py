import helper
import structures

import ctypes
import ctypes.wintypes
import sys
import win32con


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
    overlayObj.Window = ctypes.windll.user32.CreateWindowExA(win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT, overlayObj.Name, overlayObj.Name, win32con.WS_POPUP, 1, 1, overlayObj.Width, overlayObj.Height, 0, 0, hModule, 0)
    if overlayObj:
        ctypes.windll.user32.SetLayeredWindowAttributes(overlayObj.Window, ctypes.wintypes.RGB(0,0,0), 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        ctypes.windll.user32.ShowWindow(overlayObj.Window, win32con.SW_SHOW)
        ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(overlayObj.Window, ctypes.byref(overlayObj.Margin))

        return True
    
    else:
        return False


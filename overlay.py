import helper
import structures

import ctypes
import ctypes.wintypes
import sys

GWL_STYLE = -16
WS_BORDER = 0x00800000
CS_HREDRAW = 2
CS_VREDRAW = 1
IDC_ARROW = helper.MAKEINTRESOURCEA(32512)
IDI_APPLICATION = helper.MAKEINTRESOURCEA(32512)

def overlayCreateClass(winProc, windowName, hModule, overlayObj):
    overlayObj.Name = windowName.encode()
    overlayObj.Class.cbClsExtra = 0
    overlayObj.Class.cbSize = ctypes.sizeof(structures.WNDCLASSEX)
    overlayObj.Class.cbWndExtra = 0
    overlayObj.Class.hbrBackground = ctypes.windll.gdi32.CreateSolidBrush(ctypes.wintypes.RGB(0, 0, 0))
    overlayObj.Class.hCursor = ctypes.windll.user32.LoadCursorA(0, IDC_ARROW)
    overlayObj.Class.hIcon = ctypes.windll.user32.LoadIconA(0, IDI_APPLICATION)
    overlayObj.Class.hIconSm = ctypes.windll.user32.LoadIconA(0, IDI_APPLICATION)
    overlayObj.Class.hInstance = hModule
    overlayObj.Class.lpfnWndProc = winProc
    overlayObj.Class.lpszClassName = overlayObj.Name.decode()
    overlayObj.Class.lpszMenuName = overlayObj.Name.decode()
    overlayObj.Class.style = CS_HREDRAW | CS_VREDRAW

    if not ctypes.windll.user32.RegisterClassExA(ctypes.byref(overlayObj.Class)):
        return False
    
    return True



def overlayInit(overlayObj):
    window = helper.getWindow()
    size = ctypes.wintypes.RECT()

    ctypes.windll.user32.GetWindowRect(window, ctypes.byref(size))
    overlayObj.Width = size.right - size.left
    overlayObj.Height = size.bottom - size.top

    style = ctypes.windll.user32.GetWindowLongA(window, GWL_STYLE)

    if (style & WS_BORDER):
        size.top += 23
        overlayObj.Height -= 23
    
    ctypes.windll.user32.MoveWindow(overlayObj.Window, size.left, size.top, overlayObj.Width, overlayObj.Height, True)
    
    overlayObj.Margin.cxLeftWidth = 0
    overlayObj.Margin.cxRightWidth = 0
    overlayObj.Margin.cyTopHeight = overlayObj.Width
    overlayObj.Margin.cyBottomHeight = overlayObj.Height

    return True


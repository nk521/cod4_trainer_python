#pragma comment( lib, "d3d9.lib" )
#pragma comment( lib, "d3dx9.lib" )

#include <d3d9.h>
#include <d3dx9.h>
#include <windows.h>
#include <stdio.h>

#define DLL_EXPORT __declspec(dllexport)

extern "C"
{
    DLL_EXPORT void* directxInit(HWND hwnd, int overlayWidth, int overlayHeight)
    {
        IDirect3D9Ex * directxObj = 0;
        IDirect3DDevice9Ex * directxObjDevice = 0;
        D3DPRESENT_PARAMETERS directxObjParam;
        ID3DXFont * directxObjEspFont;
        ID3DXFont * directxObjFont;
        ID3DXLine * directxObjLine;

        Direct3DCreate9Ex(D3D_SDK_VERSION, &directxObj);
        ZeroMemory(&directxObjParam, sizeof(directxObjParam));
        directxObjParam.Windowed = true;
        directxObjParam.BackBufferFormat = D3DFMT_A8R8G8B8;
        directxObjParam.BackBufferHeight = overlayHeight;
        directxObjParam.BackBufferWidth = overlayWidth;
        directxObjParam.EnableAutoDepthStencil = true;
        directxObjParam.AutoDepthStencilFormat = D3DFMT_D16;
        directxObjParam.MultiSampleQuality = D3DMULTISAMPLE_NONE;
        directxObjParam.SwapEffect = D3DSWAPEFFECT_DISCARD;

        directxObj->CreateDeviceEx(D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hwnd, D3DCREATE_HARDWARE_VERTEXPROCESSING, &directxObjParam, NULL, &directxObjDevice);

        D3DXCreateFont(directxObjDevice, 20, 0, FW_BOLD, 1, false, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, DEFAULT_QUALITY, DEFAULT_PITCH | FF_DONTCARE, "Arial", &directxObjFont);
        D3DXCreateFont(directxObjDevice, 13, 0, 0, 0, false, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, DEFAULT_QUALITY, DEFAULT_PITCH, "Arial", &directxObjEspFont);

        if (!directxObjLine)
		    D3DXCreateLine(directxObjDevice, &directxObjLine);

        return directxObjDevice;
    }

    DLL_EXPORT void* directxObjDeviceBeginScene(void * ptr) {
        IDirect3DDevice9Ex * directxObjDevice = reinterpret_cast<IDirect3DDevice9Ex *>(ptr);
        directxObjDevice->BeginScene();
        return 0;
    }

    DLL_EXPORT void* directxObjDeviceEndScene(void * ptr) {
        IDirect3DDevice9Ex * directxObjDevice = reinterpret_cast<IDirect3DDevice9Ex *>(ptr);
        directxObjDevice->EndScene();
        directxObjDevice->PresentEx(0, 0, 0, 0, 0);
        directxObjDevice->Clear(0, 0, D3DCLEAR_TARGET, 0, 1.0f, 0);
        return 0;
    }
    
}
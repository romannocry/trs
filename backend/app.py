"""
# Prerequisites:
pip3 install pywin32 pyinstaller

# Build:
pyinstaller.exe --onefile --runtime-tmpdir=. --hidden-import win32timezone myservice.py
python -m PyInstaller --runtime-tmpdir=. --onefile --hidden-import win32timezone app.py

# With Administrator privilges
# Install:
dist\myservice.exe install

# Start:
dist\myservice.exe start

# Install with autostart:
dist\myservice.exe --startup delayed install

# Debug:
dist\myservice.exe debug

# Stop:
dist\myservice.exe stop

# Uninstall:
dist\myservice.exe remove
"""
import tkinter as tk
import time
import sys
import server
import os
import subprocess
import tkinter as tk
import socket
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
import win32event  # Events

class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TestService"
    _svc_display_name_ = "Test Service"
    _svc_description_ = "My service description"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        #server_path = os.path.join(sys._MEIPASS, ".\server.exe")
        server_cmd = f"call server.exe"
        self.process = subprocess.Popen(server_cmd, shell=True)
        win32event.WaitForSingleObject(self.hWaitStop   , win32event.INFINITE)

        #rc = None
        #while rc != win32event.WAIT_OBJECT_0:
        #    with open('C:\\TestService.log', 'a') as f:
        #        f.write('test service running...\n')
        #    rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)


def post_service_update(*args):
    import win32api, win32con, win32profile, pywintypes
    from contextlib import closing

    env_reg_key = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
    hkey = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, env_reg_key, 0, win32con.KEY_ALL_ACCESS)

    with closing(hkey):
        system_path = win32api.RegQueryValueEx(hkey, 'PATH')[0]
        # PATH may contain %SYSTEM_ROOT% or other env variables that must be expanded
        # ExpandEnvironmentStringsForUser(None) only expands System variables
        system_path = win32profile.ExpandEnvironmentStringsForUser(None, system_path)
        system_path_list = system_path.split(os.pathsep)

        core_dll_file = win32api.GetModuleFileName(sys.dllhandle)
        core_dll_name = os.path.basename(core_dll_file)

        for search_path_dir in system_path_list:
            try:
                dll_path = win32api.SearchPath(search_path_dir, core_dll_name)[0]
                print(f"System python DLL: {dll_path}")
                break
            except pywintypes.error as ex:
                if ex.args[1] != 'SearchPath': raise
                continue
        else:
            print("*** WARNING ***")
            print(f"Your current Python DLL ({core_dll_name}) is not in your SYSTEM PATH")
            print("The service is likely to not launch correctly.")

    from win32serviceutil import LocatePythonServiceExe
    pythonservice_exe = LocatePythonServiceExe()
    print(f"{pythonservice_exe}")
    pywintypes_dll_file = pywintypes.__spec__.origin

    pythonservice_path = os.path.dirname(pythonservice_exe)
    pywintypes_dll_name = os.path.basename(pywintypes_dll_file)

    try:
        return win32api.SearchPath(pythonservice_path, pywintypes_dll_name)[0]
    except pywintypes.error as ex:
        if ex.args[1] != 'SearchPath': raise
        print("*** WARNING ***")
        print(f"{pywintypes_dll_name} is not is the same directory as pythonservice.exe")
        print(f'Copy "{pywintypes_dll_file}" to "{pythonservice_path}"')
        print("The service is likely to not launch correctly.")

if __name__ == '__main__':
   if len(sys.argv) > 1:
       # Called by Windows shell. Handling arguments such as: Install, Remove, etc.
       win32serviceutil.HandleCommandLine(TestService,customOptionHandler=post_service_update)
   else:
       # Called by Windows Service. Initialize the service to communicate with the system operator
       servicemanager.Initialize()
       servicemanager.PrepareToHostSingle(TestService)
       servicemanager.StartServiceCtrlDispatcher()
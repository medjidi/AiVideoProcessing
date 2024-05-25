Set UAC = CreateObject("Shell.Application")
UAC.ShellExecute "cmd.exe", "/c start """" ""C:\Users\65696\PycharmProjects\Python6sem\scripts\script_server.bat""", "", "runas", 1
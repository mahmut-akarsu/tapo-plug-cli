Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = dir
pythonPath = "C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe"
shell.Run """" & pythonPath & """ -m uvicorn api:app --host 0.0.0.0 --port 8000", 0, False

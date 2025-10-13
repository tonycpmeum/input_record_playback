Write-Host "Activating virtual environment..."
. .\env\Scripts\Activate.ps1

$env:TCL_LIBRARY = "C:\Users\user\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
$env:TK_LIBRARY = "C:\Users\user\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

Write-Host "Virtual environment activated."

function sys {
   if ([System.Environment]::OSVersion.Platform -eq 'Win32NT') {
      Write-Host "machine is windows"
   } else {
      Write-Host "Machine is not windows"
   }
}

$ui = "pyside6_ui\monday"

function compileui {
   Write-Host "pyside6-uic $ui.ui -o $ui.py"
   pyside6-uic "$ui.ui" -o "$ui.py"
}
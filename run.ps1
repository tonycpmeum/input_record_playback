if (-not $env:VIRTUAL_ENV) {
   Write-Host "Activating virtual environment..."
   . .\env\Scripts\Activate.ps1

   $env:TCL_LIBRARY = "C:\Users\user\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
   $env:TK_LIBRARY = "C:\Users\user\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

   Write-Host "Virtual environment activated."
} else {
   Write-Host "Virtual environment already active."
}

function compileui {
   param(
      [string]$fileName = "mainwindow"
   )
   $ui = "pyside6_ui\$fileName"
   $outputFile = "${ui}_ui.py"
   
   Write-Host "pyside6-uic $ui.ui -o $outputFile"
   pyside6-uic "$ui.ui" -o "$outputFile"
}
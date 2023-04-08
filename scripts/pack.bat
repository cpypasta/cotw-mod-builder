echo off
del /q "%CD%\dist\modbuilder.zip"
"C:\Program Files\7-Zip\7z.exe" a -tzip "%CD%\dist\modbuilder.zip" "%CD%\dist\modbuilder"

del /q "%CD%\dist\wheel.zip"
"C:\Program Files\7-Zip\7z.exe" a -tzip "%CD%\dist\wheel.zip" "%CD%\dist\*.whl"
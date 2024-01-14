echo off
del /q "%CD%\dist\modbuilder.7z"
"C:\Program Files\7-Zip\7z.exe" a "%CD%\dist\modbuilder.7z" "%CD%\dist\modbuilder"
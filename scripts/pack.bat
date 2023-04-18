echo off
del /q "%CD%\dist\modbuilder.zip"
@REM "C:\Program Files\7-Zip\7z.exe" a -tzip "%CD%\dist\modbuilder.zip" "%CD%\dist\modbuilder"
"C:\Program Files\7-Zip\7z.exe" a "%CD%\dist\modbuilder.7z" "%CD%\dist\modbuilder"
echo off
pyinstaller --noconsole --add-data "%CD%\modbuilder\org;org" --add-data "%CD%\modbuilder\plugins\*.py;plugins" --add-data "%CD%\deca\*.py;deca" "%CD%\modbuilder.py"

del /q "%CD%\dist\modbuilder-*"
python -m build
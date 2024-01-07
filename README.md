# cotw-mod-builder

A tool that makes it easy to customize and create mods for theHunter: Call of the Wild (COTW).

![Recording](https://user-images.githubusercontent.com/2107385/230709601-c0ab9cc6-da52-4692-a82d-547b5df65cbc.gif)

Testing with game version: 2649775

## How to Build
> Note: This was built and tested with Python 3.9.6

1. Setup virtual environment _(optional; on Windows)_
```
python -m venv venv
venv\Scripts\activate
```
2. Install dependencies:
```shell
pip install -r requirements.txt
python -m PySimpleGUI.PySimpleGUI upgrade
```
3. To run the application:
```shell
python -m modbuilder
```

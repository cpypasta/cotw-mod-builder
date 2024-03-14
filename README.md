# cotw-mod-builder

A tool that makes it easy to customize and create mods for theHunter: Call of the Wild (COTW).

![Recording](https://github-production-user-asset-6210df.s3.amazonaws.com/2107385/297992314-5f7d6c72-8754-42d0-9d4a-4b7a06912b3a.png)

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

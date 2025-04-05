 #! /bin/bash
 #nuitka --standalone --onefile main.py --enable-plugin=pyside6  #--macos-app-icon=none --macos-create-app-bundle
 pyinstaller --onefile --noconsole --add-data "functions.py:." --add-data "helpers.py:." --add-data "listener.py:." main.py
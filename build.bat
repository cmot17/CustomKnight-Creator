@echo off
.\.venv\Scripts\python.exe -m nuitka --standalone --output-dir=../output --main=./main.py --output-filename="CustomKnight Creator" --windows-icon-from-ico=./resources/SheoIcon.ico --include-data-dir=./resources=resources --enable-plugin=pyside6 --windows-console-mode=disable
pause
# CustomKnight Creator

![Example Image](docs/readme_example.png)

A program to track, deduplicate, and pack sprites for use with [CustomKnight](https://github.com/PrashantMohta/HollowKnight.CustomKnight) (a Hollow Knight skin customization mod)

Inspired by [SpritePacker](https://github.com/magegihk/HollowKnight.SpritePacker) by MageGi

## Installing

* Go to the [releases](https://github.com/littlepiggeon/CustomKnight-Creator/releases) to find the latest version.

## Usage


Visit the [wiki](https://github.com/cmot17/CustomKnight-Creator/wiki) for a written tutorial.


## Running from source

* This project is built using Python 3.12.
* To run the project, just download the source code, install the dependencies [UV](https://docs.astral.sh/uv) and run main.py.
* `uv sync`

## Packaging

To package the project, use the following [nuitka](http://nuitka.net/) commands: (they are platform specific)

### Windows:
```
.\.venv\Scripts\python.exe -m nuitka --standalone --output-dir=../output --main=./main.py --output-filename="CustomKnight Creator" --windows-icon-from-ico=./resources/SheoIcon.ico --include-data-dir=./resources=resources --enable-plugin=pyside6 --windows-console-mode=disable
```

## Help

If you have any problems, feel free to open an issue on this GitHub.

## Authors
littlepiggeon(cmot17)

## License

This project is licensed under the GNU GPLv3 License - see the LICENSE.md file for details  

## At Last...
**THANKS TO cmot17!!!**

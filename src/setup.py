# -*- coding: utf-8 -*-

# Usage:
#  Packaging (Run commands from parent dir of this file):
#    - Prerequisite: `pip install --upgrade cx_Freeze`
#    - To just run a quick test for the built exe, run:          `python setup.py build`
#    - To build the full .msi (which takes ~10 sec longer) run:  `python setup.py bdist_msi`
#  Icon Files:
#    Icon Creation:
#      - .png or .ico -> Resized .ico: https://www.aconvert.com/icon/
#      - .ico -> .png: https://cloudconvert.com/ico-to-png
#      - Looks best if img is square, PowerPoint w/ right-click "Size & Position" is good enough for me at least
#    Additional Icon File Doc:
#      - There are many icons/imgs that could all be made different but for simplicity have been set up to be the same
#      - The best way to do this is to have the same image file in 2 formats:
#        - .ico - Required for .exe, .msi, and .lnk icons
#        - .png - For the image that appears in the top left of the Tkinter GUI and the in the taskbar
#          - Not technically required but recommended:
#            - It is possible to use the same .ico for the GUI, but .png is better for some complicated sub-gui reason
#              - (See gui.py for details)

# Future Improvements:
#  - Add option to prompt user to open program after install
#    - https://cx-freeze-users.narkive.com/xThwhu4x/cx-freeze-bdist-msi-install-script-option

# Other Useful Links:
#   - cx_freeze setup script doc - https://cx-freeze.readthedocs.io/en/latest/setup_script.html

from pprint import pprint
from typing import List, Tuple
from cx_Freeze import setup, Executable
from pathlib import Path
import sys
import cfg
from os.path import relpath
import uuid

SCRIPT_PARENT_DIR_PATH = Path(__file__).parent

# base="Win32GUI" should be used only for Windows GUI app
BASE = "Win32GUI" if sys.platform == "win32" else None

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#  .msi / .exe / General Dist. Inputs (Also see cfg.py)
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

PRODUCT_DESCRIPTION = 'Uses exports from QuickEMR & opentimeclock.com to calculate employee productivity'

TOP_LEVEL_PY_FILE_PATH = SCRIPT_PARENT_DIR_PATH  / "gui.py"

EXE_ICON_ICO_PATH = SCRIPT_PARENT_DIR_PATH / "imgs" / "icon.ico"
GUI_ICON_PNG_PATH = SCRIPT_PARENT_DIR_PATH / "imgs" / "icon.png"

EXE_ICON_ICO_PATH_REL_TO_EXE_PARENT_DIR = "imgs/icon.ico"#FIXME

# DATA_FILE_PATHS:
# - Paths to non-python data/config files that need to be copied to the build dir so they will be accessible by the
#   python script files after freeze.
#     - Icon image paths used for the GUI for example
# - To keep things simple, the paths of all "data files" will be re-created such that the relative paths of each
#   original "data file" to this file before freezing (./imgs/icon.png for example) will be the same as the relative
#   paths of each copied-over/included "data file" relative to the created .exe after freezing.
# - Additionally, (also to keep things simple) when the .msi is created, it will include everything in/under the
#   parent dir of the created .exe
# - THEREFORE TO KEEP THINGS SIMPLE, `DATA_FILE_PATHS` should not include paths to files above this file's parent dir.
DATA_FILE_PATHS = [
    GUI_ICON_PNG_PATH,
    EXE_ICON_ICO_PATH# FIX?
]

ADD_DESKTOP_SHORTCUT_FROM_MSI = True
ADD_START_MENU_SHORTCUT_FROM_MSI = True # Adds to "Recently Added"
ADD_STARTUP_SHORTCUT_FROM_MSI = False # Only use if program should run on startup

SHOW_CMD = True # Useful for testing - Seems to be broken?

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# Derived Constants
EXE_FILE_NAME = cfg.PRODUCT_NAME + ".exe"

# See `_get_shortcut_table()` for doc
COMMON_SHORTCUT_TABLE_TUP = (
    cfg.PRODUCT_NAME,              # Name that will be show on the link
    "TARGETDIR",                   # Component_
    f"[TARGETDIR]{EXE_FILE_NAME}", # Target exe to execute
    None,                          # Arguments
    PRODUCT_DESCRIPTION,           # Description
    None,                          # Hotkey
    # EXE_ICON_ICO_PATH.as_posix(),  # Icon
    f"[TARGETDIR]{EXE_ICON_ICO_PATH_REL_TO_EXE_PARENT_DIR}",  # Icon
    None,                          # IconIndex
    SHOW_CMD,                      # ShowCmd
    'TARGETDIR'                    # WkDir
)


def _get_input_file_tups_from_data_file_paths(data_file_paths: List[Path]) -> List[Tuple[str, str]]:
    """
    (This example assumes this file exists at c/p/myapp/src/setup.py)
    Input: [Path("c/p/myapp/src/imgs/gui_icon.png"), Path("c/p/myapp/src/config/some_file.txt")]
    Output:
    [
        ("c/p/myapp/src/imgs/gui_icon.png", "imgs/gui_icon.png"),
        ("c/p/myapp/src/config/some_file.txt", "config/some_file.txt"),
    ]
    """
    return [(data_file_path.as_posix(), relpath(data_file_path.as_posix(), SCRIPT_PARENT_DIR_PATH.as_posix())) for data_file_path in data_file_paths]


def _get_shortcut_table():
    """
    This gets into the Windows shortcut / directory tables, seems complicated, never dove very deep into this, probably
    possible to do more useful things here.
      - http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
      - List of possible values for Directory_:
          - https://learn.microsoft.com/en-us/windows/win32/msi/property-reference?redirectedfrom=MSDN#system-folder-properties
    It is technically possible to set a different icon, target, args, etc. for each shortcut, but to keep things simple,
    everything other than the first 2 items (Shortcut & Directory_) comes from a common derived constant
    """
    shortcut_table = []

    if ADD_DESKTOP_SHORTCUT_FROM_MSI:
        # Example: C:\Users\Bob\Desktop\MyGreatShortcut.lnk
        shortcut_table.append(
            (
                "DesktopShortcut",             # Shortcut (Not sure if the exact name matters for this)
                "DesktopFolder",               # Directory_
            ) + COMMON_SHORTCUT_TABLE_TUP
        )
    if ADD_START_MENU_SHORTCUT_FROM_MSI:
        # Example: C:\Users\Bob\AppData\Roaming\Microsoft\Windows\Start Menu\MyGreatShortcut.lnk
        shortcut_table.append(
            (
                "StartMenuShortcut",           # Shortcut (Not sure if the exact name matters for this)
                "StartMenuFolder",             # Directory_
            ) + COMMON_SHORTCUT_TABLE_TUP
        )
    # Wont automatically Pin shortcut to start menu, but will make it appear in the "Recently Added" section in the top
    # right of the start menu with a right-click option to pin
    if ADD_STARTUP_SHORTCUT_FROM_MSI:
        # Example: C:\Users\Bob\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\MyGreatShortcut.lnk
        shortcut_table.append(
            (
                "StartupShortcut",             # Shortcut (Not sure if the exact name matters for this)
                "StartupFolder",               # Directory_
            ) + COMMON_SHORTCUT_TABLE_TUP
        )

    return shortcut_table


# Setup keyword options: https://cx-freeze.readthedocs.io/en/latest/keywords.html
setup(
    author="Brandon Valley",
    # author_email="",
    # url="",
    # download_url="",
    name=cfg.PRODUCT_NAME,
    version=cfg.PRODUCT_VERSION_STR,
    description=PRODUCT_DESCRIPTION,
    executables=[
        Executable(
            script = TOP_LEVEL_PY_FILE_PATH,
            target_name = EXE_FILE_NAME,
            copyright="Copyright (C) 2024 PuffinPublishing",
            base=BASE,
            icon=EXE_ICON_ICO_PATH,

            # # Cant use the same shortcut_dir here as used for msi or it will throw error 2756
            # shortcut_name="ProductivityCalculatorStartMenuShortcut",
            # shortcut_dir="ProgramFilesFolder",
        )
    ],

    options={
        "build_exe": {
            "include_files": _get_input_file_tups_from_data_file_paths(DATA_FILE_PATHS),

            # # Haven't needed these options yet, but I think they're for including/excluding python files?
            # "includes": ["abc"],
            # "excludes": [i for i in AllPackage() if notFound(BasicPackages,i)],
            # "zip_include_packages": ["encodings"] ##
        },

        # Change some default MSI options and specify the use of the above defined tables
        'bdist_msi': {
            'data': {
                # Create the table dictionary
                "Shortcut": _get_shortcut_table(),
                # https://stackoverflow.com/questions/68539511/is-there-a-way-to-update-application-created-with-cx-freeze
                # 'upgrade_code': '{3F2504E0-4F89-11D3-9A0C-0305E82C3301}',
                # 'add_to_path': False,
            }
        }
    }
)

print(f"\nDone! Output written to {SCRIPT_PARENT_DIR_PATH}/dist/{cfg.PRODUCT_NAME}-{cfg.PRODUCT_VERSION_STR}-win64.msi")
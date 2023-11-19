# -*- coding: utf-8 -*-

# Usage:
#  - To just run a quick test for the built exe, run:  `python setup.py build`
#  - To build the full .msi (which takes ~10 sec longer) run:  `python setup.py bdist_msi`

# Future Improvements:
#  - Add option to prompt user to open program after install
#    - https://cx-freeze-users.narkive.com/xThwhu4x/cx-freeze-bdist-msi-install-script-option

from typing import List, Tuple
from cx_Freeze import setup, Executable
from pathlib import Path
import sys
import cfg
from os.path import relpath

SCRIPT_PARENT_DIR_PATH = Path("__file__").parent

# base="Win32GUI" should be used only for Windows GUI app
BASE = "Win32GUI" if sys.platform == "win32" else None

########################################################################################################################
# Inputs
########################################################################################################################

PRODUCT_DESCRIPTION = 'Uses exports from QuickEMR & opentimeclock.com to calculate employee productivity'

TOP_LEVEL_PY_FILE_PATH = SCRIPT_PARENT_DIR_PATH  / "gui.py"

EXE_ICON_ICO_PATH = SCRIPT_PARENT_DIR_PATH / "imgs" / "icon.ico"
GUI_ICON_PNG_PATH = SCRIPT_PARENT_DIR_PATH / "imgs" / "icon.png"

# Paths to non-python data/config files that need to be copied to the build dir so they will be accessible by the python
# script files after freeze. - icon image paths used for the GUI for example
DATA_FILE_PATHS = [
    GUI_ICON_PNG_PATH
]

ADD_DESKTOP_SHORTCUT_FROM_MSI = True
ADD_STARTUP_SHORTCUT_FROM_MSI = False
ADD_START_MENU_SHORTCUT_FROM_MSI = False

SHOW_CMD = False # Useful for testing


ICON_PNG_STR_PATH = "imgs//icon.png" # FIX rename to rel pat?

# Derived
EXE_FILE_NAME = cfg.PRODUCT_NAME + ".exe"


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
    """ http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx """
    shortcut_table = []

    if ADD_DESKTOP_SHORTCUT_FROM_MSI:
        shortcut_table.append(
            (
                "DesktopShortcut",        # Shortcut
                "DesktopFolder",          # Directory_
                cfg.PRODUCT_NAME,           # Name that will be show on the link
                "TARGETDIR",              # Component_
                f"[TARGETDIR]{EXE_FILE_NAME}",     # Target exe to execute # FIX
                None,                     # Arguments
                PRODUCT_DESCRIPTION,      # Description
                None,                     # Hotkey
                EXE_ICON_ICO_PATH.as_posix(),                     # Icon
                None,                     # IconIndex
                SHOW_CMD,                 # ShowCmd
                'TARGETDIR'               # WkDir
            )
        )
    if ADD_STARTUP_SHORTCUT_FROM_MSI:
        shortcut_table.append(
            (
                "StartupShortcut",        # Shortcut
                "StartupFolder",          # Directory_
                cfg.PRODUCT_NAME,           # Name that will be show on the link
                "TARGETDIR",              # Component_
                f"[TARGETDIR]{EXE_FILE_NAME}",     # Target exe to execute # FIX
                None,                     # Arguments
                PRODUCT_DESCRIPTION,      # Description
                None,                     # Hotkey
                EXE_ICON_ICO_PATH.as_posix(),                     # Icon
                None,                     # IconIndex
                SHOW_CMD,                 # ShowCmd
                'TARGETDIR'               # WkDir
            )
        )
    if ADD_START_MENU_SHORTCUT_FROM_MSI:
        # Possible solution: https://github.com/marcelotduarte/cx_Freeze/issues/48
        raise NotImplementedError("Pinning the shortcut to start from msi is not yet implemented")

    return shortcut_table




# Now create the table dictionary
msi_data = {"Shortcut": _get_shortcut_table()}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}


setup(
    name=cfg.PRODUCT_NAME,
    version=cfg.PRODUCT_VERSION_STR,
    description=PRODUCT_DESCRIPTION,
    executables=[
        Executable(
            script = TOP_LEVEL_PY_FILE_PATH,
            target_name = EXE_FILE_NAME,
            # copyright="Copyright (C) 2024 cx_Freeze",
            base=BASE,
            icon=EXE_ICON_ICO_PATH, # DOC https://www.freeconvert.com/png-to-ico/download

            # # Cant use the same shortcut_dir here as used for msi or it will throw error 2756
            # shortcut_name="ProductivityCalculatorStartMenuShortcut",
            # shortcut_dir="ProgramFilesFolder",
        )
    ],

    options={
        "build_exe": {
            # "includes": BasicPackages,
            # "excludes": [i for i in AllPackage() if notFound(BasicPackages,i)],
            "include_files": _get_input_file_tups_from_data_file_paths(DATA_FILE_PATHS)
            
            # [
            #     (ICON_PNG_STR_PATH, "imgs/icon.png") # Include .png icon for GUI to use
            #     ],
            # "zip_include_packages": ["encodings"] ##
        },

        'bdist_msi': bdist_msi_options,

    }
)

print(f"Done! Output written to {SCRIPT_PARENT_DIR_PATH}/dist/{cfg.PRODUCT_NAME}-{cfg.PRODUCT_VERSION_STR}-win64.msi")
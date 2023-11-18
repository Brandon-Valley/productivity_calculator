# -*- coding: utf-8 -*-


# Usage:
#  - To just run a quick test for the built exe, run:  `python setup.py build`
#  - To build the full .msi (which takes ~10 sec longer) run:  `python setup.py bdist_msi`

# https://stackoverflow.com/questions/57339138/msi-created-in-cx-freeze-does-not-install-program
# msiexec -i "Productivity Calculator-0.0.3-win64.msi" -l*vx log.txt


from cx_Freeze import setup, Executable
from pathlib import Path
import sys

SCRIPT_PARENT_DIR_PATH = Path("__file__").parent


# base="Win32GUI" should be used only for Windows GUI app
BASE = "Win32GUI" if sys.platform == "win32" else None

PRODUCT_NAME = "Productivity Calculator"
PRODUCT_DESCRIPTION = 'Uses exports from QuickEMR & opentimeclock.com to calculate employee productivity'
ICON_STR_PATH = "imgs//icon.ico" # FIX rename to rel pat? 
ICON_PNG_STR_PATH = "imgs//icon.png" # FIX rename to rel pat? 



# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
# https://github.com/marcelotduarte/cx_Freeze/issues/48
# shortcut_table = [
#     (
#         "DesktopShortcut",        # Shortcut
#      "DesktopFolder",          # Directory_
#      PRODUCT_NAME,           # Name that will be show on the link
#      "TARGETDIR",              # Component_
#      "[TARGETDIR]gui.exe",# Target exe to execute
#      None,                     # Arguments
#      PRODUCT_DESCRIPTION,                      # Description # FIX?
#      None,                     # Hotkey
#      "imgs//icon.ico",                     # Icon
#      None,                     # IconIndex
#      True,                     # ShowCmd
#      'TARGETDIR'               # WkDir
#      )
#     ]
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "program",     # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]gui.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),

    # For adding separate shortcut to Startup folder so the program will run whenever PC is restarted

    # ("StartupShortcut",        # Shortcut
    #  "StartupFolder",          # Directory_
    #  "program",     # Name
    #  "TARGETDIR",              # Component_
    #  "[TARGETDIR]main.exe",   # Target
    #  None,                     # Arguments
    #  None,                     # Description
    #  None,                     # Hotkey
    #  None,                     # Icon
    #  None,                     # IconIndex
    #  None,                     # ShowCmd
    #  'TARGETDIR'               # WkDir
    #  ),
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

# options = {
#     'bdist_msi': bdist_msi_options
# }
#     #   # Comment this out if only want exe & run with: python setup.py build
#     #   options={
#     #       'bdist_msi': bdist_msi_options, # if need msi - run with: python setup.py bdist_msi
#     #     #   'build_exe': build_exe_options # If dont need msi
#     #       }   
#       )

setup(
    name=PRODUCT_NAME,
    version='0.0.5',
    description=PRODUCT_DESCRIPTION,
    executables=[
        Executable(
            SCRIPT_PARENT_DIR_PATH  / "gui.py",
            # copyright="Copyright (C) 2024 cx_Freeze",
            base=BASE,
            icon="imgs//icon.ico", # DOC https://www.freeconvert.com/png-to-ico/download
            shortcut_name=PRODUCT_NAME,
            shortcut_dir="MyProgramMenu",
        ),
    ],
    options={
    "build_exe": {
        # "includes": BasicPackages,
        # "excludes": [i for i in AllPackage() if notFound(BasicPackages,i)],
        "include_files": [
            (ICON_PNG_STR_PATH, "imgs/icon.png") # Include .png icon for GUI to use
            ],
        # "zip_include_packages": ["encodings"] ##
    },
    'bdist_msi': bdist_msi_options
}
)


































# if __name__ == "__main__":
#     import os.path as path
#     import subprocess
#     subprocess.call("python setup.py build", shell=True)
#     # print("Running " , path.abspath(__file__) , '...')

#     # print("End of Main") 





# # -*- coding: utf-8 -*-

# # A simple setup script to create an executable using Tkinter. This also
# # demonstrates the method for creating a Windows executable that does not have
# # an associated console.
# #
# # SimpleTkApp.py is a very simple type of Tkinter application
# #
# # Run the build process by running the command 'python setup.py build'
# #
# # If everything works well you should find a subdirectory in the build
# # subdirectory that contains the files needed to run the application


# # https://cx-freeze.readthedocs.io/en/stable/setup_script.html#setup-script

# import sys
# from cx_Freeze import setup, Executable

# # https://stackoverflow.com/questions/17307934/creating-msi-with-cx-freeze-and-bdist-msi-for-pyside-app

# product_name = "Sample_TK_App"


# base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'


# # # "C:\Users\Brandon\AppData\Local\Programs\Python\Python39\Lib\site-packages\cx_Freeze\command\bdist_msi.py"
# # bdist_msi_options = {
# #     # 'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
# #     'add_to_path': False,
# #     'initial_target_dir': r'[ProgramFilesFolder]\%s' % (product_name),
# #     }


# # build_exe_options = {
# #     # 'includes': ['atexit', 'PySide.QtNetwork'],
# #     }


# # https://stackoverflow.com/questions/15734703/use-cx-freeze-to-create-an-msi-that-adds-a-shortcut-to-the-desktop


# # http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
# shortcut_table = [
#     ("DesktopShortcut",        # Shortcut
#      "DesktopFolder",          # Directory_
#      "My SimpleTkApp from msi",           # Name that will be show on the link
#      "TARGETDIR",              # Component_
#      "[TARGETDIR]SimpleTkApp.exe",# Target exe to execute
#      None,                     # Arguments
#      None,                     # Description
#      None,                     # Hotkey
#      None,                     # Icon
#      None,                     # IconIndex
#      None,                     # ShowCmd
#      'TARGETDIR'               # WkDir
#      )
#     ]

# # Now create the table dictionary
# msi_data = {"Shortcut": shortcut_table}

# # Change some default MSI options and specify the use of the above defined tables
# bdist_msi_options = {'data': msi_data}



# executables = [
#     Executable('SimpleTkApp.py', base=base)
# ]

# setup(name='simple_Tkinter',
#       version='0.1',
#       description='Sample cx_Freeze Tkinter script',
#       executables=executables,

#     #   # Comment this out if only want exe & run with: python setup.py build
#     #   options={
#     #       'bdist_msi': bdist_msi_options, # if need msi - run with: python setup.py bdist_msi
#     #     #   'build_exe': build_exe_options # If dont need msi
#     #       }   
#       )


















# from cx_Freeze import setup, Executable

# # Dependencies are automatically detected, but it might need
# # fine tuning.
# build_options = {'packages': [], 'excludes': []}

# import sys
# base = 'Win32GUI' if sys.platform=='win32' else None

# executables = [
#     Executable('"C:\\p\\productivity_calculator\\src\\gui.py"', base=base, target_name = 'Productivity_Calculator.exe')
# ]

# setup(name='Productivity Calculator',
#       version = '0.0.1',
#       description = 'Uses exports from QuickEMR & opentimeclock.com to calculate employee productivity',
#       options = {'build_exe': build_options},
#       executables = executables)

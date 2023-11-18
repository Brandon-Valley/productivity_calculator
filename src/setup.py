# -*- coding: utf-8 -*-

# relimport.py is a very simple script that tests importing using relative
# imports (available in Python 2.5 and up)
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable
from pathlib import Path

SCRIPT_PARENT_DIR_PATH = Path("__file__").parent

executables = [
    # Executable(SCRIPT_PARENT_DIR_PATH / "src" / "gui.py")
    Executable(SCRIPT_PARENT_DIR_PATH  / "gui.py")
]

setup(name='Productivity Calculator',
      version='0.1.0',
      description='Uses exports from QuickEMR & opentimeclock.com to calculate employee productivity',
      executables=executables
      )







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

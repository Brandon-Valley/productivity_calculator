"""Contains common vars, mostly for use by setup.py & gui.py"""

from pathlib import Path
import sys

# def _get_data_dir_path():
#     """
#     Returns dir path from which paths to data files like icons should be based - needed for after freezing w/ cx_freeze
#       - This assumes the data files have been added to the build dir when setup.py was run
#     """
#     if getattr(sys, 'frozen', False):
#         # The application is frozen
#         #   - sys.executable is the path to the .exe created by cx_freeze
#         return Path(sys.executable).parent
#     else:
#         # The application is not
#         print("not frozen")
#         return SCRIPT_PARENT_DIR_PATH

PRODUCT_VERSION_STR = "0.0.9"
PRODUCT_NAME = "Productivity Calculator"
IMGS_DIR_PATH = Path("__file__").parent / "imgs"
GUI_ICON_PNG_PATH =  IMGS_DIR_PATH / "icon.png"

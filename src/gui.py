# taskkill /im python.exe /F

from __future__ import absolute_import
import os
from pathlib import Path
import sys

from tkinter.ttk import *
from tkinter import *

import cfg
from   sms.GUI_tools import GUI_tools_utils as gtu
import Main_Tab

SCRIPT_PARENT_DIR_PATH = Path(__file__).parent


def _get_data_dir_path():
    """
    Returns dir path from which paths to data files like icons should be based - needed for after freezing w/ cx_freeze
      - This assumes the data files have been added to the build dir when setup.py was run
    """
    if getattr(sys, 'frozen', False):
        # The application is frozen
        #   - sys.executable is the path to the .exe created by cx_freeze
        return Path(sys.executable).parent
    else:
        # The application is not
        print("not frozen")
        return SCRIPT_PARENT_DIR_PATH

def main(msg = None):
    # Main GUI params
    window_title = f"{cfg.PRODUCT_NAME} v{cfg.PRODUCT_VERSION_STR}"
    want_duplicate_apps_to_stack_in_toolbar = True

    data_dir_path = _get_data_dir_path()
    print(f"{data_dir_path=}")

    # Set to None for default iconphoto
    # Can work with either .png or .ico, but if you use a .ico, you need to pass the photo_img_path down to all sub-guis,
    # no clue why but will only inherit iconphoto (png), not iconbitmap(ico) from gui with same app_id
    iconphoto_abs_path_str = (data_dir_path / "imgs" / "icon.png").as_posix()

    # Secondary gui params

    # If you do not set the app_id:
    #     - if no iconphoto is set, tool bar image will be default python, instead of tk feather
    #     - duplicate applications will stack, but you will be unable to stack additional applications, such as a child msg_box
    set_app_id = True

    # Highest level GUI must always use TK(), not Toplevel(), PhotoImage can only work after TK(), but if this has
    # already been called in a higher level GUI, use Toplevel()
    # Running with Toplevel as your root GUI will also make a blank window appear
    master = Tk()
    master.title(window_title)

    #Get and set app_id
    if set_app_id:
        app_id = gtu.get_app_id_unique_to_this_file(__file__, want_duplicate_apps_to_stack_in_toolbar)
        gtu.set_app_id(app_id)
    else:
        app_id = None

    # Set iconphoto
    gtu.set_iconphoto_if_not_None(master, iconphoto_abs_path_str)

    # Tab_control
    tab_control = Notebook(master)
    tab_control.grid(row=1, column=0, sticky='NESW')

    Main_Tab.Main_Tab(master, tab_control, iconphoto_abs_path_str, app_id)

    master.mainloop()





if __name__ == '__main__':
    main()
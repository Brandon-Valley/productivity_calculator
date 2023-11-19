# taskkill /im python.exe /F

from __future__ import absolute_import
from datetime import datetime
import os
from pathlib import Path
import sys
import time

from tkinter.ttk import *
from tkinter import *
from tkinter.messagebox import showerror
import traceback

import cfg
from   sms.GUI_tools import GUI_tools_utils as gtu
from   sms.file_system_utils import file_system_utils as fsu
import Main_Tab

import logging

SCRIPT_PARENT_DIR_PATH = Path(__file__).parent

# import ctypes# TMP
# MessageBox = ctypes.WinDLL('user32').MessageBoxW

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
    


def _set_up_logging(log_file_parent_dir_path: Path, max_old_log_file_age_sec: int = 2628288) -> Path:# FIX add delete old
    """2628288 sec ~= 1 month"""
    # Delete any log files older than max_old_log_file_age_sec
    if log_file_parent_dir_path:
        for path_obj in log_file_parent_dir_path.glob("*"):
            num_sec_since_last_modified = int(time.time() - os.path.getmtime(path_obj))
            if max_old_log_file_age_sec < num_sec_since_last_modified:
                os.remove(path_obj)

    if log_file_parent_dir_path:
        log_file_parent_dir_path.mkdir(parents=True, exist_ok=True)

    log_file_name = cfg.PRODUCT_NAME.replace(" ", "_") + "_" + datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S') + ".log"
    log_file_path = log_file_parent_dir_path / log_file_name

    logging.root.handlers = []
    logging.basicConfig(
        level=logging.INFO,
        # format="%(asctime)s [%(levelname)s] %(message)s",
        format="%(message)s",
        handlers=[logging.FileHandler(log_file_path), logging.StreamHandler(sys.stdout)]
    )
    logging.info(f"Initialized logging for {log_file_path=}...\n")
    return log_file_path



def main(msg = None):
    data_dir_path = _get_data_dir_path()
    print(f"{data_dir_path=}")


    _log_file_path = _set_up_logging(data_dir_path / "logs")

    # Main GUI params
    window_title = f"{cfg.PRODUCT_NAME}  v{cfg.PRODUCT_VERSION_STR}"
    want_duplicate_apps_to_stack_in_toolbar = True

    # Set to None for default iconphoto
    # Can work with either .png or .ico, but if you use a .ico, you need to pass the photo_img_path down to all sub-guis,
    # no clue why but will only inherit iconphoto (png), not iconbitmap(ico) from gui with same app_id
    iconphoto_abs_path_str = (data_dir_path / "imgs" / "icon.png").as_posix()

    # Secondary gui params

    # If you do not set the app_id:
    #     - if no iconphoto is set, tool bar image will be default python, instead of tk feather
    #     - duplicate applications will stack, but you will be unable to stack additional applications, such as a child msg_box
    set_app_id = True

    # Show popup w/ traceback on raised exception
    def _report_callback_exception(self, exc, val, tb):
        showerror("Error", message=traceback.format_exc())
    Tk.report_callback_exception = _report_callback_exception

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
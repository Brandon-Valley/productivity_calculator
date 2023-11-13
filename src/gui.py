# taskkill /im python.exe /F


from tkinter.ttk import *
from tkinter import *

from sms.GUI_tools import GUI_tools_utils as gtu

import Main_Tab



def main(msg = None): 
    # main gui params
    window_title = "Setup New Repository"
    want_duplicate_apps_to_stack_in_toolbar = True
    
    # set to None for default iconphoto
    # can work with either .png or .ico, but if you use a .ico, you need to pass the photo_img_path down to all sub-guis,
    # no clue why but will only inherit iconphoto (png), not iconbitmap(ico) from gui with same app_id    
    iconphoto_rel_to_this_file_path = 'imgs//icon.png' 
    
    # secondary gui params
    
    # if you do not set the app_id:                                                             
    #     - if no iconphoto is set, tool bar image will be default python, instead of tk feather
    #     - duplicate applications will stack, but you will be unable to stack additional applications, such as a child msg_box                                               
    set_app_id = True
                      
                      
    # highest level GUI must always use TK(), not Toplevel(), PhotoImage can only work after TK(), but if this has already been called in a higher level GUI, use Toplevel()
    # running with Toplevel as your root GUI will also make a blank window appear
    master = Tk()
    master.title(window_title)

    # get and set app_id
    if set_app_id:
        app_id = gtu.get_app_id_unique_to_this_file(__file__, want_duplicate_apps_to_stack_in_toolbar)
        gtu.set_app_id(app_id)
    else:
        app_id = None
    
    # get and set iconphoto
    iconphoto_abs_path = gtu.rel_path_to_this_file__to__abs_path__if_not_None(__file__, iconphoto_rel_to_this_file_path)
    gtu.set_iconphoto_if_not_None(master, iconphoto_abs_path)
      
    # tab_control
    tab_control = Notebook(master)
    tab_control.grid(row=1, column=0, sticky='NESW')
    
    Main_Tab.Main_Tab(master, tab_control, iconphoto_abs_path, app_id)

    master.mainloop()
 

 

 
if __name__ == '__main__':
    main()
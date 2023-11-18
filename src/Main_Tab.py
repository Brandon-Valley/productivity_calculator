# taskkill /im python.exe /F

from datetime import datetime
import os
from pathlib import Path
from tkinter.ttk import *
from tkinter import *
import subprocess



# if __name__ == "__main__": 
from   sms.GUI_tools                             import Tab
from   sms.GUI_tools.run_func_with_loading_popup import run_func_with_loading_popup
from   sms.msg_box_utils                         import msg_box_utils               as mbu
from   main import main

# else:
#     from . sms.GUI_tools                             import Tab
#     from . sms.GUI_tools.run_func_with_loading_popup import run_func_with_loading_popup
#     from . sms.msg_box_utils                         import msg_box_utils               as mbu
#     from . main import main

# # from   sms.logger                                import json_logger
# from   sms.GUI_tools                             import Tab
# from   sms.GUI_tools.run_func_with_loading_popup import run_func_with_loading_popup
# # from   sms.clipboard_utils                       import clipboard_utils             as cbu
# from   sms.msg_box_utils                         import msg_box_utils               as mbu
# # import                                                  common_vars                 as cv


DOWNLOADS_DIR_PATH_STR = str(Path.home() / "Downloads") 
DEFAULT_OUTPUT_PARENT_DIR_PATH = Path.home() / "Documents" / "Productivity_Reports"
DEFAULT_OUTPUT_FILE_NAME = f"Productivity_Report_{datetime.today().strftime('%Y-%m-%d')}.csv"

SETUP_NEW_REPO_SCRIPT_ABS_PATH = os.path.dirname(os.path.abspath(__file__)) + '//setup_new_repo.py'

# GUI_VARS_JSON_PATH = cv.PROGRAM_DATA_DIR_PATH + '\\setup_new_repo_gui_vars.json'

# REPO_TYPE_CBOX_VALUES = [cv.REPO_TYPE_KEY__IP, cv.REPO_TYPE_KEY__PIC, cv.REPO_TYPE_KEY__OTHER]
REPO_TYPE_CBOX_VALUES = ["a", "b", "c"]

KNOWN_ERROR_CODE_MSG_D = {128: 'fatal: remote error: Repository not found.  The requested repository does not exist, or you do not have permission to access it.'}

REMOTE_URL_TB_WIDTH = 77 # the width of the whole window is dependent on this value, as long as it is => 77

DEFAULT_FONT_STR              = 'Helvetica 9'
REMOTE_WARNING_FINAL_FONT_STR = 'Helvetica 10 bold'



class Main_Tab(Tab.Tab):
    def __init__(self, master, tab_control, photo_img_path = None, app_id = None):
        Tab.Tab.__init__(self, master, tab_control, photo_img_path, app_id)

        self.app_id = app_id

        # self.read_gui_vars()

        self.calculate_btn_____widget_setup()
        self.inputs_____widget_setup()
        self.output_____widget_setup()
        self.update_calculate_btn_disable_tool_tip_and_state()

        self.grid_init_widgets()



    # def read_gui_vars(self):
    #     self.gui_vars_d = json_logger.read(GUI_VARS_JSON_PATH, return_if_file_not_found = None)

    #     if self.gui_vars_d == None:
    #         self.gui_vars_d = {}

    # def write_gui_var(self, key_str, val):
    #     self.gui_vars_d[key_str] = val
    #     json_logger.write(self.gui_vars_d, GUI_VARS_JSON_PATH)

    # def get_gui_var(self, key_str):
    #     if key_str in self.gui_vars_d.keys():
    #         return self.gui_vars_d[key_str]
    #     else:
    #         return ''



    def inputs_____widget_setup(self):

        def _get_updated_tooltip_existing_csv_only(report_name, fsb_widget):
            file_path = Path(fsb_widget.tb.get())
            if file_path.suffix.lower() == ".csv":
                if file_path.is_file():
                    return ''
                else:
                    return f'{report_name} ({file_path}) does not exist.'
            else:
                return f'{report_name} must be an existing .csv file.'
            
        
        # Tool Tip reasons
        self.provider_prod_csv_export_disable_tool_tip_reason__csv_only = ''
        self.payroll_csv_export_disable_tool_tip_reason__csv_only = ''

        def _update_provider_prod_csv_export_tooltip_csv_only(event = None):
            self.provider_prod_csv_export_disable_tool_tip_reason__csv_only = _get_updated_tooltip_existing_csv_only(
                report_name="The Quick EMR Provider Productivity Export",
                fsb_widget=self.provider_prod_fsb_wg,
            )
            self.update_calculate_btn_disable_tool_tip_and_state()

        def _update_payroll_csv_export_tooltip_csv_only(event = None):
            self.payroll_csv_export_disable_tool_tip_reason__csv_only = _get_updated_tooltip_existing_csv_only(
                report_name="Open Time Clock PayrollExcel Export (Converted to .csv)",
                fsb_widget=self.payroll_fsb_wg,
            )
            self.update_calculate_btn_disable_tool_tip_and_state()
          

        # Label Frame
        self.inputs_lbl_frm = LabelFrame(self.master, text=" Inputs: ")

        # Quick EMR Provider Productivity
        self.provider_prod_fsb_wg = self.File_System_Browse_WG(self.inputs_lbl_frm,
                                                         lbl_txt = 'Quick EMR Export: Provider Productivity CSV:',
                                                         tb_width = 80,
                                                         browse_for = 'file',
                                                         file_type = '.csv',
                                                         init_path=DOWNLOADS_DIR_PATH_STR,
                                                         focus_tb_after_browse = True,
                                                         tb_edit_func = _update_provider_prod_csv_export_tooltip_csv_only)
        self.provider_prod_fsb_wg.tb.delete(0, 'end')
        self.provider_prod_fsb_wg.tb.insert(END, "")

        # OpenTimeClock Payroll
        self.payroll_fsb_wg = self.File_System_Browse_WG(self.inputs_lbl_frm,
                                                         lbl_txt = 'Open Time Clock Export: PayrollExcel (Converted to .csv):',
                                                         tb_width = 80,
                                                         browse_for = 'file',
                                                         file_type = '.csv',
                                                         init_path=DOWNLOADS_DIR_PATH_STR,
                                                         focus_tb_after_browse = True,
                                                         tb_edit_func = _update_payroll_csv_export_tooltip_csv_only)
        self.payroll_fsb_wg.tb.delete(0, 'end')
        self.payroll_fsb_wg.tb.insert(END, "")

        # Update all
        _update_provider_prod_csv_export_tooltip_csv_only()
        _update_payroll_csv_export_tooltip_csv_only()




    def output_____widget_setup(self):

        # Label Frame
        self.output_lbl_frm = LabelFrame(self.master, text=" Output: ")

        # Quick EMR Provider Productivity
        self.output_pdfn_wg = self.Write_Parent_Dir_File_Name_WG(
                                                                    self.output_lbl_frm,
                                                                    parent_dir_lbl_txt = "Output Parent Folder:",
                                                                    file_name_lbl_txt = "Output File Name:",
                                                                    parent_dir_tb_width = None,
                                                                    file_name_tb_width = 30,
                                                                    init_parent_dir_path_str = DEFAULT_OUTPUT_PARENT_DIR_PATH, #FIX replace with gui var?
                                                                    init_file_name = DEFAULT_OUTPUT_FILE_NAME,
                                                                    write_file_path_updated_func = None,# FIXME?
                                                                    focus_parent_dir_tb_after_browse = False,
                                                                    browse_btn_txt = 'Browse...',
                                                                    parent_dir_tb_edit_func = None,# FIX?
                                                                    file_path_tb_edit_func = None,# FIX?
                                                                )
  


    def calculate_btn_____widget_setup(self):

        def calculate_btn_clk():
            

            # Do thing#FIX
            print("CLICK")

            output_report_file_path_str = self.output_pdfn_wg.write_file_path_str
            main(
                exported_open_time_clock_payroll_csv_path=Path(self.payroll_fsb_wg.tb.get()),
                quick_emr_provider_productivity_csv_path=Path(self.provider_prod_fsb_wg.tb.get()),
                output_report_file_path=Path(output_report_file_path_str)
            )

            reveal_in_file_explorer = mbu.msg_box__YES_NO(
                title='Success!',
                msg=(
                    f'Calculated Productivity Report has been written to: {output_report_file_path_str}'
                    "\n\n Reveal in File Explorer?"
                ),
                    icon = 'info',
                    app_id = self.app_id
            )

            if reveal_in_file_explorer:
                subprocess.Popen(f'explorer /select,"{output_report_file_path_str}"')

            # Exit gracefully
            exit()



        self.calculate_btn = Button(self.master, text="Calculate Productivity", wraplength = 90, command = calculate_btn_clk)



    def update_calculate_btn_disable_tool_tip_and_state(self):

        def add_to_text_if_not_empty(text, str):
            if str == '':
                return text

            if text != '':
                text += '\n'
            return text+ '- ' + str

        text = ''

        # All vars wont already be initialized first time through
        try:
            text = add_to_text_if_not_empty(text, self.provider_prod_csv_export_disable_tool_tip_reason__csv_only)
            text = add_to_text_if_not_empty(text, self.payroll_csv_export_disable_tool_tip_reason__csv_only)
            print(f"{text=}")

            self.calculate_btn_tool_tip = self.Tool_Tip(self.calculate_btn, text = text, wait_time = 0, wrap_length = 200)

        except AttributeError:
            pass

        if text == '':
            self.calculate_btn.configure(state = 'normal')
        else:
            self.calculate_btn.configure(state = 'disabled')



    def grid_init_widgets(self):
        self.master.grid_columnconfigure(1, weight=1) # Used to allow column 1 in root to expand as window resized


        # --------------------------------------------------------------------------------------------------------------
        #  Inputs
        # --------------------------------------------------------------------------------------------------------------
        
        # Sticky WE here lets the LabelFrame Expand as the window is resized
        self.inputs_lbl_frm      .grid(column=1, row=2, padx=5, pady=5, sticky='WE') 

         # Used to allow column 2 (w/ the Entry Widget) in root to expand as LabelFrame resized
        self.inputs_lbl_frm.grid_columnconfigure(2, weight=1)

        self.provider_prod_fsb_wg.lbl   .grid(column=1 , row=1, padx=5, pady=5, sticky='E')
        self.provider_prod_fsb_wg.tb    .grid(column=2 , row=1, padx=5, pady=5, sticky='WE')
        self.provider_prod_fsb_wg.btn   .grid(column=4 , row=1, padx=5, pady=5, sticky='E')

        self.payroll_fsb_wg.lbl   .grid(column=1 , row=2, padx=5, pady=5, sticky='E')
        self.payroll_fsb_wg.tb    .grid(column=2 , row=2, padx=5, pady=5, sticky='WE')
        self.payroll_fsb_wg.btn   .grid(column=4 , row=2, padx=5, pady=5, sticky='E')

        # --------------------------------------------------------------------------------------------------------------
        #  Output
        # --------------------------------------------------------------------------------------------------------------

        # Sticky WE here lets the LabelFrame Expand as the window is resized
        self.output_lbl_frm      .grid(column=1, row=3, padx=5, pady=5, sticky='WE') 

         # Used to allow column 2 (w/ the Entry Widget) in root to expand as LabelFrame resized
        self.output_lbl_frm.grid_columnconfigure(2, weight=1)

        self.output_pdfn_wg.parent_dir_lbl   .grid(column=1 , row=3, padx=5, pady=5, sticky='E')
        self.output_pdfn_wg.parent_dir_tb    .grid(column=2 , row=3, padx=5, pady=5, sticky='WE')
        self.output_pdfn_wg.btn              .grid(column=4 , row=3, padx=5, pady=5, sticky='E')

        self.output_pdfn_wg.file_name_lbl       .grid(column=1 , row=4, padx=5, pady=5, sticky='E')
        self.output_pdfn_wg.file_name_tb        .grid(column=2 , row=4, padx=5, pady=5, sticky='WE')

        self.output_pdfn_wg.write_file_path_descrip_lbl .grid(column=1 , row=5, padx=5, pady=5, sticky='E')
        self.output_pdfn_wg.write_file_path_lbl         .grid(column=2 , row=5, padx=5, pady=5, sticky='W', columnspan = 4)


        # --------------------------------------------------------------------------------------------------------------
        #  Calculate
        # --------------------------------------------------------------------------------------------------------------
        self.calculate_btn  .grid(column=1, row=4, padx=5, pady=5, sticky='E')




if __name__ == '__main__':
    import gui
    gui.main()
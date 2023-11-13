

from datetime import datetime
from pathlib import Path
from pprint import pprint
import file_io_utils

ROW_TYPE_PROVIDER_NAME = "PROVIDER_NAME"
ROW_TYPE_DATE_DATA = "DATE_DATA"

def get_total_units_dict_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path: Path, facility_names) -> dict:
    # """
    # Example output:
    # {
    #     Gates SLP, Bill {
    #         datetime(2023-20-10): {
    #             total_units: 4,
    #             total_unts
    #         }
    #     }
    # }
    
    # """
    
    def _get_row_type(row_dict):
        if "Total for" not in row_dict["Prov/Facility"] and row_dict["Prov/Facility"] not in ["", "UNITS/Visits", "Grand Total"] + facility_names:
            return ROW_TYPE_PROVIDER_NAME
        elif "/" in row_dict["DOS"]:
            return ROW_TYPE_DATE_DATA
        return None




    total_units_dict_by_date_by_provider_name = {}

    row_dicts = file_io_utils.read_csv_as_row_dicts(in_csv_path)
    # print(row_dicts)
    # print("row_dicts:")
    # pprint(row_dicts)

    cur_provider_name = None
    for row_dict in row_dicts:

        row_type = _get_row_type(row_dict)

        # Set row_type
        # if "Total for" not in row_dict["Prov/Facility"] and row_dict["Prov/Facility"] not in ["", "UNITS/Visits", "Grand Total"] + facility_names:
        #     return ROW_TYPE_PROVIDER_NAME
        # elif "/" in row_dict["DOS"]:
        #     return ROW_TYPE_DATE_DATA
        # return None






        # Set cur_provider_name if needed
        if row_type == ROW_TYPE_PROVIDER_NAME:
            cur_provider_name = row_dict["Prov/Facility"]
            total_units_dict_by_date_by_provider_name[cur_provider_name] = {}

        # Set cur_provider_name if needed
        if row_type == ROW_TYPE_DATE_DATA:
            cur_provider_name = row_dict["Prov/Facility"]
            total_units_dict_by_date_by_provider_name[cur_provider_name] = {}

            date_datetime = datetime.strptime(row_dict["DOS"], '%Y-%m-%d')

        









    return total_units_dict_by_date_by_provider_name

if __name__ == "__main__":
    SCRIPT_PARENT_DIR_PATH = Path('__file__').parent#os.path.abspath(os.path.dirname("__file__"))
    # WRK_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "wrk"
    # MY_PAYROLL_CSV_PATH = WRK_DIR_PATH / "my_payroll.csv"
    # ROW_DICTS_TMP_JSON_PATH = WRK_DIR_PATH / "otc_row_dicts.json"

    import os.path as path
    print("Running ",  path.abspath(__file__), '...')

    in_csv_path = Path("C:/p/productivity_calculator/inputs/Provider Productivity 10_16.csv")
    out = get_total_units_dict_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path,
                                                                                              facility_names = ["TP1"])
    
    print("out:")
    pprint(out)
    print("End of Main") 
    
    
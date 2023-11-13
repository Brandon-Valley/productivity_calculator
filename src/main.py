


from pathlib import Path
from pprint import pprint
from open_time_clock_utils import get_payroll_data_dict_by_employee_name
from quick_emr_utils import get_productivity_data_dicts_by_date_by_provider_name_from_provider_productivity_csv_export

FACILITY_NAMES = ["TP1"]

# WRK_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "wrk"

def main(exported_open_time_clock_payroll_csv_path, quick_emr_provider_productivity_csv_path):
    print("Parsing payroll CSV...")
    payroll_data_dict_by_employee_name = get_payroll_data_dict_by_employee_name(exported_open_time_clock_payroll_csv_path)
    print(f"{payroll_data_dict_by_employee_name=}")

    prod_data_dicts_by_date_by_provider_name = get_productivity_data_dicts_by_date_by_provider_name_from_provider_productivity_csv_export(
        quick_emr_provider_productivity_csv_path, FACILITY_NAMES)
    print(f"{prod_data_dicts_by_date_by_provider_name=}")




if __name__ == "__main__":

    import os.path as path
    print("Running ",  path.abspath(__file__), '...')

    # in_csv_path = Path("C:/p/productivity_calculator/inputs/Provider Productivity 10_16.csv")
    # out = get_productivity_data_dicts_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path,
    #                                                                                           facility_names = ["TP1"])

    main(exported_open_time_clock_payroll_csv_path = Path("C:/p/productivity_calculator/inputs/exported_PayrollExcel_10_16.csv"),
         quick_emr_provider_productivity_csv_path = Path("C:/p/productivity_calculator/inputs/Provider Productivity 10_16.csv"))
    
    # print("out:")
    # pprint(out)
    print("End of Main") 
    


from pathlib import Path
import pprint
import file_io_utils


def get_total_units_dict_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path: Path) -> dict:
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

    row_dicts = file_io_utils.read_csv_as_row_dicts(in_csv_path)
    # print(row_dicts)






if __name__ == "__main__":
    SCRIPT_PARENT_DIR_PATH = Path('__file__').parent#os.path.abspath(os.path.dirname("__file__"))
    # WRK_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "wrk"
    # MY_PAYROLL_CSV_PATH = WRK_DIR_PATH / "my_payroll.csv"
    # ROW_DICTS_TMP_JSON_PATH = WRK_DIR_PATH / "otc_row_dicts.json"

    import os.path as path
    print("Running ",  path.abspath(__file__), '...')

    in_csv_path = Path("C:/p/productivity_calculator/inputs/exported_PayrollExcel_10_16.csv")
    out = get_total_units_dict_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path)
    
    # print("out:")
    # pprint(out)
    print("End of Main") 
    
    
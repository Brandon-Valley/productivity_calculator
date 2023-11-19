from datetime import datetime, timedelta
import os
from pathlib import Path
from pprint import pprint
import file_io_utils


SCRIPT_PARENT_DIR_PATH = Path('__file__').parent
# WRK_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "wrk"
# MY_PAYROLL_CSV_PATH = WRK_DIR_PATH / "my_payroll.csv"#TMP
MY_PAYROLL_CSV_PATH = Path("C:/p/productivity_calculator/src/wrk/my_payroll.csv")
# ROW_DICTS_TMP_JSON_PATH = WRK_DIR_PATH / "otc_row_dicts.json"

class CsvWriteFailedException(Exception):
    pass


def _get_date_range_tup(in_csv_path):
    lines = file_io_utils.read_lines_from_txt(in_csv_path)
    print(f"{lines[1]=}")
    
    # Example: 'Date range:,2023-10-16  -  2023-10-27'
    date_range_line = lines[1]
    start_date_str = date_range_line.split(",")[1].split("  -  ")[0]
    end_date_str = date_range_line.split(",")[1].split("  -  ")[1]
    
    return (datetime.strptime(start_date_str, '%Y-%m-%d'), datetime.strptime(end_date_str, '%Y-%m-%d'))


def _write_my_payroll_csv(start_datetime, end_datetime, in_csv_path, out_csv_path):
    with open(in_csv_path) as textFile:  # can throw FileNotFoundError
        lines =  list(l.rstrip() for l in textFile.readlines())
        
        init_header_line = lines[2]
        data_lines = lines[3:]
        print(f"{init_header_line=}")
        
    day_strs = init_header_line.split("Department,Employee Number,Employee Name,")[1].split(",Basic Hours")[0].split(",")
    print(f"{day_strs=}")
    
    num_days_timedelta = start_datetime - end_datetime
    num_days_int = num_days_timedelta.days * -1
    print(f"{num_days_timedelta=}")
    print(f"{num_days_int=}")
    
    assert num_days_int + 1 == len(day_strs), f"{num_days_int + 1=} != {len(day_strs)=}, {day_strs} - Something wrong with date range?"
    
    # build date_strs
    date_strs = []
    for i in range(num_days_int + 1):
        new_datetime = start_datetime + timedelta(days=i)
        date_strs.append(new_datetime.strftime('%Y-%m-%d'))
    
    print(f"{date_strs=}")
    assert end_datetime.strftime('%Y-%m-%d') == date_strs[-1], f"{end_datetime.strftime('%Y-%m-%d')=} == {date_strs[-1]=}"

    # Build new_header_line
    og_day_strs_str = ",".join(day_strs)
    print(f"\n{og_day_strs_str=}\n")
    new_date_strs_str = ",".join(date_strs)
    new_header_line = init_header_line.replace(og_day_strs_str, new_date_strs_str)
    assert new_header_line != init_header_line, f"{new_header_line=} == {init_header_line=}"
    print(f"")
    print(f"{new_header_line=}")
    
    # Write new csv
    new_csv_lines = [new_header_line] + data_lines
    
    try:
        with open(out_csv_path, "w") as textFile:  # can throw FileNotFoundError
            for line in new_csv_lines:
                textFile.writelines(line.replace(",", ",") + "\n")
    except PermissionError as e:
        raise CsvWriteFailedException(
            f"ERROR: Got PermissionError when trying to write {out_csv_path}, "
            "This is probably because the file is open in Excel. Close file and try again"
        ) from e


def _get_payroll_data_dict_by_employee_name_from_my_payroll_csv(in_csv_path):
    payroll_data_dict_by_employee_name = {}
    
    row_dicts = file_io_utils.read_csv_as_row_dicts(in_csv_path) 
    
    for row_dict in row_dicts:
        employee_name = row_dict["Employee Name"]
        
        assert employee_name not in payroll_data_dict_by_employee_name, "This func. assumes each employee name only appears on one row, will need to rewrite if this is not the case"
        
        if employee_name not in payroll_data_dict_by_employee_name:
            payroll_data_dict_by_employee_name[employee_name] = {}
        
        row_dict.pop("Employee Name")
        payroll_data_dict_by_employee_name[employee_name] = row_dict
        
    return payroll_data_dict_by_employee_name


def get_payroll_data_dict_by_employee_name(in_csv_path, working_payroll_csv_path = MY_PAYROLL_CSV_PATH, delete_working_payroll_csv_path = False):
    """in_csv_path - Path to CSV created by exporting default PayrollExcel.xlsx downloaded from OpenTimeClock"""
    print(f"in get_payroll_data_dict_by_employee_name - {in_csv_path=}")
    # row_dicts = file_io_utils.read_csv_as_row_dicts(in_csv_path)
    # file_io_utils.write_json(row_dicts, ROW_DICTS_TMP_JSON_PATH)#TMP
    
    start_datetime, end_datetime = _get_date_range_tup(in_csv_path)
    print(f"{(start_datetime, end_datetime)=}")
    
    _write_my_payroll_csv(start_datetime, end_datetime, in_csv_path, working_payroll_csv_path)
    assert working_payroll_csv_path.is_file(), working_payroll_csv_path
    print(f"Wrote {working_payroll_csv_path=}")
    
    payroll_data_dict_by_employee_name = _get_payroll_data_dict_by_employee_name_from_my_payroll_csv(working_payroll_csv_path)
    
    if delete_working_payroll_csv_path:
        os.remove(working_payroll_csv_path)
        
    return payroll_data_dict_by_employee_name


def get_hours_by_date_by_employee_name(in_csv_path, working_payroll_csv_path = MY_PAYROLL_CSV_PATH, delete_working_payroll_csv_path = False):
    hours_by_date_by_employee_name = {}
    payroll_data_dict_by_employee_name = get_payroll_data_dict_by_employee_name(in_csv_path, working_payroll_csv_path, delete_working_payroll_csv_path)

    for employee_name, payroll_data_dict in payroll_data_dict_by_employee_name.items():
        hours_by_date_by_employee_name[employee_name] = {}

        for k, v in payroll_data_dict.items():

            # If date_str column
            if k.count("-") == 2:
                
                datetime_date = datetime.strptime(k, '%Y-%m-%d') # str -> datetime
                hours = float(v)
                hours_by_date_by_employee_name[employee_name][datetime_date] = hours

    return hours_by_date_by_employee_name







if __name__ == "__main__":
    import os.path as path
    print("Running ",  path.abspath(__file__), '...')

    in_csv_path = Path("C:/p/productivity_calculator/inputs/exported_PayrollExcel_10_16.csv")
    # payroll_data_dict_by_employee_name = get_payroll_data_dict_by_employee_name(in_csv_path)
    
    # print("payroll_data_dict_by_employee_name:")
    # pprint(payroll_data_dict_by_employee_name)
    out = get_hours_by_date_by_employee_name(in_csv_path)
    
    print("out:")
    pprint(out)
    print("End of Main") 
    
    
    

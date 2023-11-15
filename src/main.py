


from pathlib import Path
from pprint import pprint
from file_io_utils import write_csv_from_row_dicts
from open_time_clock_utils import get_hours_by_date_by_employee_name
from quick_emr_utils import get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export

FACILITY_NAMES = ["TP1"]

OUTPUT_REPORT_ORDERED_HEADERS = ["Employee Name", "Date", "Hours Worked", "Total Units", "Max Possible Units for Number of Hours Worked", "Calculated Productivity %"]

# WRK_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "wrk"

def _write_productivity_report(hours_by_date_by_employee_name, total_units_by_date_by_provider_name, output_report_file_path):
    # def _get_normalized_provider_name_plus_title(provider_name):
    #     last_name_plus_title, first_name = provider_name.split(",")
    #     return first_name + last_name_plus_title

    def _get_provider_name_by_employee_name():
        provider_name_by_employee_name = {}

        for employee_name, _hours_by_date in hours_by_date_by_employee_name.items():
            for provider_name, _total_units_by_date in total_units_by_date_by_provider_name.items():
                print(f"{provider_name.split(',')=}")
                first_name = provider_name.split(",")[-1].strip()
                name_suffix = " ".join(provider_name.split(",")[:-1])
                normalized_provider_name_plus_title = first_name +  " " + name_suffix
                print(f"{normalized_provider_name_plus_title=}")
                print(f"{employee_name=}")

                if normalized_provider_name_plus_title.startswith(employee_name):
                    assert employee_name not in provider_name_by_employee_name, (
                        f"ERROR, {employee_name=} already in {provider_name_by_employee_name=}, found while handling "
                        f"{normalized_provider_name_plus_title=}. Something is wrong with name mapping, look at new hire names?"
                    )
                    provider_name_by_employee_name[employee_name] = provider_name
            
            print(f"Employee: {employee_name} does not appear in Provider Productivity report, skipping...")

            # assert employee_name in provider_name_by_employee_name, (
            #     f"ERROR: {employee_name=} NOT in {provider_name_by_employee_name=}, Something is wrong with name mapping, look at new hire names?"
            # )

        return provider_name_by_employee_name
            
    
    # Build provider_name_by_employee_name
    provider_name_by_employee_name = _get_provider_name_by_employee_name()
    print("provider_name_by_employee_name:")
    pprint(provider_name_by_employee_name)



    # Build row_dicts
    row_dicts = []
    for employee_name, hours_by_date in hours_by_date_by_employee_name.items():
        if employee_name not in provider_name_by_employee_name:
            print(f"{employee_name=} not in provider_name_by_employee_name, skipping...")
            continue

        for date_datetime, hours in hours_by_date.items():

            provider_name = provider_name_by_employee_name[employee_name]
            try:
                total_units = total_units_by_date_by_provider_name[provider_name][date_datetime]
            except KeyError:
                print(f"Got KeyError on {date_datetime=} in total_units_by_date_by_provider_name, must be a non-working day, skipping...")
                continue
            
            new_row_dict = {
                "Employee Name": employee_name,
                "Date": date_datetime.strftime('%Y-%m-%d'),
                "Hours Worked": hours,
                "Total Units": total_units
            }


        print(f"{new_row_dict=}")

# OUTPUT_REPORT_ORDERED_HEADERS = ["Employee Name", "Date", "Hours Worked", "Total Units", "Max Possible Units for Number of Hours Worked", "Calculated Productivity %"]

    row_dicts = {}








    # write_csv_from_row_dicts(row_dicts, csv_path, ordered_headers: Optional[List[str]])



def main(exported_open_time_clock_payroll_csv_path, quick_emr_provider_productivity_csv_path, output_report_file_path):
    print("Parsing payroll CSV...")
    hours_by_date_by_employee_name = get_hours_by_date_by_employee_name(exported_open_time_clock_payroll_csv_path)
    print(f"{hours_by_date_by_employee_name=}")

    total_units_by_date_by_provider_name = get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export(
        quick_emr_provider_productivity_csv_path, FACILITY_NAMES)
    print(f"{total_units_by_date_by_provider_name=}")

    _write_productivity_report(
        hours_by_date_by_employee_name,
        total_units_by_date_by_provider_name,
        output_report_file_path)


    # FIX todo

    # from my_payroll - for each name for each day (like AH 10/16/2023 = 6.93) * 4 (b/c thats the max units that COULD have been billed / hr)
    # then summ all UNITS per provider / day from provider Productivity  csv
    # then just sz sum / (6.93 * 4)



if __name__ == "__main__":

    import os.path as path
    print("Running ",  path.abspath(__file__), '...')

    main(exported_open_time_clock_payroll_csv_path = Path("C:/p/productivity_calculator/inputs/exported_PayrollExcel_10_16.csv"),
         quick_emr_provider_productivity_csv_path = Path("C:/p/productivity_calculator/inputs/Provider Productivity 10_16.csv"),
         output_report_file_path="C:/p/productivity_calculator/wrk/out.csv")

    print("End of Main") 
    
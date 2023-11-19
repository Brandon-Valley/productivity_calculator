


from pathlib import Path
from pprint import pprint
import logging
from file_io_utils import write_csv_from_row_dicts
from open_time_clock_utils import get_hours_by_date_by_employee_name
from quick_emr_utils import get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export




MAX_POSSIBLE_UNITS_PER_HOUR = 4

FACILITY_NAMES = ["TP1"]

OUTPUT_REPORT_ORDERED_HEADERS = ["Employee Name", "Date", "Hours Worked", "Total Units", "Max Possible Units for Number of Hours Worked", "Calculated Productivity %"]


def _write_productivity_report(hours_by_date_by_employee_name, total_units_by_date_by_provider_name, output_report_file_path):

    def _get_provider_name_by_employee_name():
        provider_name_by_employee_name = {}

        for employee_name, _hours_by_date in hours_by_date_by_employee_name.items():
            for provider_name, _total_units_by_date in total_units_by_date_by_provider_name.items():
                logging.info(f"{provider_name.split(',')=}")
                first_name = provider_name.split(",")[-1].strip()
                name_suffix = " ".join(provider_name.split(",")[:-1])
                normalized_provider_name_plus_title = first_name +  " " + name_suffix
                logging.info(f"{normalized_provider_name_plus_title=}")
                logging.info(f"{employee_name=}")

                if normalized_provider_name_plus_title.startswith(employee_name):
                    assert employee_name not in provider_name_by_employee_name, (
                        f"ERROR, {employee_name=} already in {provider_name_by_employee_name=}, found while handling "
                        f"{normalized_provider_name_plus_title=}. Something is wrong with name mapping, look at new hire names?"
                    )
                    provider_name_by_employee_name[employee_name] = provider_name
            
            logging.info(f"Employee: {employee_name} does not appear in Provider Productivity report, skipping...")

        return provider_name_by_employee_name
            
    logging.info(f"{hours_by_date_by_employee_name=}")
    logging.info(f"{total_units_by_date_by_provider_name=}")
    # Build provider_name_by_employee_name
    provider_name_by_employee_name = _get_provider_name_by_employee_name()
    logging.info(f"{provider_name_by_employee_name=}")
    logging.info("provider_name_by_employee_name:")

    # Build row_dicts
    row_dicts = []
    for employee_name, hours_by_date in hours_by_date_by_employee_name.items():
        if employee_name not in provider_name_by_employee_name:
            logging.info(f"{employee_name=} not in provider_name_by_employee_name, skipping...")
            continue

        for date_datetime, hours in hours_by_date.items():

            provider_name = provider_name_by_employee_name[employee_name]
            try:
                total_units = total_units_by_date_by_provider_name[provider_name][date_datetime]
            except KeyError:
                logging.info(f"Got KeyError on {date_datetime=} in total_units_by_date_by_provider_name, must be a non-working day, skipping...")
                continue

            max_units = hours * MAX_POSSIBLE_UNITS_PER_HOUR
            
            row_dicts.append(
                {
                    "Employee Name": employee_name,
                    "Date": date_datetime.strftime('%Y-%m-%d'),
                    "Hours Worked": hours,
                    "Total Units": total_units,
                    "Max Possible Units for Number of Hours Worked": max_units,
                    "Calculated Productivity %": round((total_units / max_units) * 100, 2)
                }
            )

    write_csv_from_row_dicts(row_dicts, output_report_file_path, OUTPUT_REPORT_ORDERED_HEADERS)


def calculate_productivity(exported_open_time_clock_payroll_csv_path, quick_emr_provider_productivity_csv_path, output_report_file_path):
    logging.info("Parsing payroll CSV...")
    hours_by_date_by_employee_name = get_hours_by_date_by_employee_name(exported_open_time_clock_payroll_csv_path)
    logging.info(f"{hours_by_date_by_employee_name=}")

    total_units_by_date_by_provider_name = get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export(
        quick_emr_provider_productivity_csv_path, FACILITY_NAMES)
    logging.info(f"{total_units_by_date_by_provider_name=}")

    logging.info("Calculating productivity & producing report...")
    _write_productivity_report(
        hours_by_date_by_employee_name,
        total_units_by_date_by_provider_name,
        output_report_file_path)
    
    assert output_report_file_path.is_file(), output_report_file_path
    logging.info(f"Success! Report written to {output_report_file_path}")


if __name__ == "__main__":

    import os.path as path
    logging.info("Running ",  path.abspath(__file__), '...')

    calculate_productivity(exported_open_time_clock_payroll_csv_path = Path("C:/p/productivity_calculator/inputs/exported_PayrollExcel_10_16.csv"),
         quick_emr_provider_productivity_csv_path = Path("C:/p/productivity_calculator/inputs/Provider Productivity 10_16.csv"),
         output_report_file_path=Path("C:/p/productivity_calculator/wrk/out.xlsx"))

    logging.info("End of Main") 
    
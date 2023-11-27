


from pathlib import Path
from pprint import pprint
import logging
from file_io_utils import write_csv_from_row_dicts
from open_time_clock_utils import get_hours_by_date_by_employee_name
from quick_emr_utils import get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export

try:
    from override_provider_name_by_employee_name import OVERRIDE_PROVIDER_NAME_BY_EMPLOYEE_NAME
except ModuleNotFoundError:
    logging.info("No override file found.")


MAX_POSSIBLE_UNITS_PER_HOUR = 4

FACILITY_NAMES = ["TP1"]

OUTPUT_REPORT_ORDERED_HEADERS = ["Employee Name", "Date", "Hours Worked", "Total Units", "Max Possible Units for Number of Hours Worked", "Calculated Productivity %"]


def _write_productivity_report(hours_by_date_by_employee_name, total_units_by_date_by_provider_name, output_report_file_path):

    # def _get_provider_name_by_employee_name__full_name_match_method():
    #     provider_name_by_employee_name = {}

    #     for employee_name in hours_by_date_by_employee_name.keys():
    #         for provider_name in total_units_by_date_by_provider_name.keys():
    #             logging.info(f"{provider_name.split(',')=}")
    #             first_name = provider_name.split(",")[-1].strip()
    #             name_suffix = " ".join(provider_name.split(",")[:-1])
    #             normalized_provider_name_plus_title = first_name +  " " + name_suffix
    #             logging.info(f"{normalized_provider_name_plus_title=}")
    #             logging.info(f"{employee_name=}")

    #             if normalized_provider_name_plus_title.startswith(employee_name):
    #                 assert employee_name not in provider_name_by_employee_name, (
    #                     f"ERROR, {employee_name=} already in {provider_name_by_employee_name=}, found while handling "
    #                     f"{normalized_provider_name_plus_title=}. Something is wrong with name mapping, look at new hire names?"
    #                 )
    #                 provider_name_by_employee_name[employee_name] = provider_name

    #         logging.info(f"Employee: {employee_name} does not appear in Provider Productivity report, skipping...")

    #     return provider_name_by_employee_name

    def _get_provider_name_by_employee_name():
        """First names might be different, assume last names same"""
        provider_name_by_employee_name = {}

        for employee_name in hours_by_date_by_employee_name.keys():
            print(f"{employee_name=}")
            last_names = [] # for error checking

            for provider_name in total_units_by_date_by_provider_name.keys():
                logging.info(f"{provider_name.split(',')=}")
                # first_name = provider_name.split(",")[-1].strip().lower()
                name_suffix = " ".join(provider_name.split(",")[:-1]).lower()
                last_name = name_suffix.split(" ")[0].lower()

                # Check if 2 ppl have same last name
                assert last_name not in last_names, f"ERROR: 2 Providers have the same last name: {last_name=}, {last_names=}"
                last_names.append(last_name)

                try:
                    if employee_name in OVERRIDE_PROVIDER_NAME_BY_EMPLOYEE_NAME:
                        provider_name_by_employee_name[employee_name] = OVERRIDE_PROVIDER_NAME_BY_EMPLOYEE_NAME[employee_name]
                        continue
                # If no override file
                except NameError:
                    pass

                if employee_name.lower().endswith(last_name):
                    assert employee_name not in provider_name_by_employee_name, (
                        f"ERROR, {employee_name=} already in {provider_name_by_employee_name=}, found while handling "
                        f"{last_name=}. Something is wrong with name mapping, look at new hire names?"
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

            if hours == 0:
                logging.info(f"{hours=}, this means {employee_name} did not come in at all for the time period, they "
                             "will not appear in the output csv, skipping...")
                continue

            provider_name = provider_name_by_employee_name[employee_name]
            try:
                total_units = total_units_by_date_by_provider_name[provider_name][date_datetime]
            except KeyError:
                logging.info(f"Got KeyError on {date_datetime=} in total_units_by_date_by_provider_name, must be a non-working day, skipping...")
                continue

            max_units = hours * MAX_POSSIBLE_UNITS_PER_HOUR

            calculated_productivity_percent = round((total_units / max_units) * 100, 0)
            assert calculated_productivity_percent <= 100, f"{calculated_productivity_percent=}, {employee_name=}, {date_datetime=}"

            row_dicts.append(
                {
                    "Employee Name": employee_name,
                    "Date": date_datetime.strftime('%Y-%m-%d'),
                    "Hours Worked": hours,
                    "Total Units": total_units,
                    "Max Possible Units for Number of Hours Worked": max_units,
                    "Calculated Productivity %": calculated_productivity_percent
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

    # calculate_productivity(exported_open_time_clock_payroll_csv_path = Path("C:/p/productivity_calculator/inputs/exported_PayrollExcel_10_16.csv"),
    #      quick_emr_provider_productivity_csv_path = Path("C:/p/productivity_calculator/inputs/Provider Productivity 10_16.csv"),
    calculate_productivity(exported_open_time_clock_payroll_csv_path = Path("C:/Users/Brandon/Downloads/KjpbmSeS.csv"),
         quick_emr_provider_productivity_csv_path = Path("C:/Users/Brandon/Downloads/Provider Productivity.csv"),
         output_report_file_path=Path("C:/p/productivity_calculator/wrk/out.csv"))

    logging.info("End of Main")

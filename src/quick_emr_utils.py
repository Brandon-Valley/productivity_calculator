

from datetime import datetime
from pathlib import Path
import logging
from pprint import pformat
from pprint import pprint
from typing import List

import file_io_utils

PROVIDER_PRODUCTIVITY_HEADER_NAMES = [
    "Provider Details",
    "Facility",
    "DOS",
    "POS",
    "Type",
    "Units",
    "Units To Bill",
]

ROW_TYPE_FACILITY_NAME = "FACILITY_NAME"
ROW_TYPE_PROVIDER_NAME = "PROVIDER_NAME"
ROW_TYPE_DATE_DATA = "DATE_DATA"

def _get_productivity_data_dicts_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path: Path, facility_names) -> dict:
    """
    Example input csv:

    | Provider Details   | Facility | DOS                                 | POS       | Type | Units | Units To Bill |
    |--------------------|----------|-------------------------------------|-----------|------|-------|---------------|
    | Green OT, John     | TP1      | [07/19/2024](note_228122)           | 11: Office| OT   | 5     | 1             |
    | Lee SLP, Bruce     | TP1      | [07/19/2024](note_228075)           | 11: Office| ST   | 4     | 4             |
    | Lee SLP, Bruce     | TP1      | [07/11/2024](note_226711)           | 11: Office| ST   | 4     | 4             |

    Example output:
    {
        'Green OT, John': {datetime.datetime(2024, 6, 11, 0, 0): [{'POS': '11: '
                                                                        'Office',
                                                                'Type': 'OT',
                                                                'Units': '2',
                                                                'Units To Bill': '2'},
                                                                {'POS': '11: '
                                                                        'Office',
                                                                'Type': 'OT',
                                                                'Units': '4',
                                                                'Units To Bill': '4'},
    }
    """
    def _validate_provider_productivity_csv_format(row_dicts: List[dict]) -> None:
        try:
            first_row_headers = list(row_dicts[0].keys())
        except IndexError:
            raise ValueError(f"Format Error: {in_csv_path=} - CSV is empty")
        
        assert (h in first_row_headers for h in PROVIDER_PRODUCTIVITY_HEADER_NAMES), (
            f"Format Error: {in_csv_path=} - CSV is missing one or more expected headers from "
            f"{PROVIDER_PRODUCTIVITY_HEADER_NAMES}="
        )
        
        assert len(first_row_headers) == len(PROVIDER_PRODUCTIVITY_HEADER_NAMES), (
            f"Format Error: {in_csv_path=} - CSV has a different number of headers than expected: {first_row_headers=} "
            f"vs. {PROVIDER_PRODUCTIVITY_HEADER_NAMES=}"
        )

        for row_dict in row_dicts:
            for key, value in row_dict.items():
                assert (value != "" and value != None), f"Format Error: {in_csv_path=} - CSV has blank value at {key=}"



    row_dicts = file_io_utils.read_csv_as_row_dicts(in_csv_path)

    logging.info(f"Validating {in_csv_path=}...")
    _validate_provider_productivity_csv_format(row_dicts)

    exit("here")
    # def _get_row_type(row_dict: dict):

    #     assert type(row_dict) is dict, row_dict

    #     row_is_blank = True

    #     for v in row_dict.values():
    #         if v != "":
    #             row_is_blank = False
    #     if row_is_blank:
    #         return None

    #     if row_dict["Prov/Facility"] in facility_names:
    #         return ROW_TYPE_FACILITY_NAME

    #     elif "Total for" not in row_dict["Prov/Facility"] and \
    #         row_dict["Prov/Facility"] not in ["", "UNITS/Visits", "Grand Total"] + facility_names and \
    #         not row_dict["DOS"]:

    #         return ROW_TYPE_PROVIDER_NAME
    #     elif "/" in row_dict["DOS"]:
    #         return ROW_TYPE_DATE_DATA
    #     return None


    # total_units_dict_by_date_by_provider_name = {}

    # row_dicts = file_io_utils.read_csv_as_row_dicts(in_csv_path)

    # cur_provider_name = None
    # for row_dict in row_dicts:
    #     print("row_dict:")
    #     pprint(row_dict)

    #     row_type = _get_row_type(row_dict)

    #     # Set cur_provider_name if needed
    #     if row_type == ROW_TYPE_PROVIDER_NAME:
    #         new_provider_name = row_dict["Prov/Facility"]
    #         cur_provider_name = new_provider_name
    #         total_units_dict_by_date_by_provider_name[cur_provider_name] = {}

    #     # Set cur_provider_name if needed
    #     if row_type == ROW_TYPE_DATE_DATA:
    #         date_datetime = datetime.strptime(row_dict["DOS"], '%m/%d/%Y')

    #         if date_datetime not in total_units_dict_by_date_by_provider_name[cur_provider_name]:
    #             total_units_dict_by_date_by_provider_name[cur_provider_name][date_datetime] = []

    #         row_dict.pop("Prov/Facility")
    #         row_dict.pop("DOS")
    #         total_units_dict_by_date_by_provider_name[cur_provider_name][date_datetime].append(row_dict)

    # return total_units_dict_by_date_by_provider_name



def get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path: Path, facility_names):
    logging.info("in get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export")

    total_units_by_date_by_provider_name = {}
    productivity_data_dicts_by_date_by_provider_name = _get_productivity_data_dicts_by_date_by_provider_name_from_provider_productivity_csv_export(
        in_csv_path, facility_names)
    
    pprint(productivity_data_dicts_by_date_by_provider_name)#TMP

    for provider_name, productivity_data_dicts_by_date in productivity_data_dicts_by_date_by_provider_name.items():
        total_units_by_date_by_provider_name[provider_name] = {}

        for date_datetime, productivity_data_dicts in productivity_data_dicts_by_date.items():
            total_units_by_date_by_provider_name[provider_name][date_datetime] = 0
            for productivity_data_dict in productivity_data_dicts:
                total_units_by_date_by_provider_name[provider_name][date_datetime] += int(productivity_data_dict["Units"])

    return total_units_by_date_by_provider_name



if __name__ == "__main__":
    SCRIPT_PARENT_DIR_PATH = Path('__file__').parent

    import os.path as path
    logging.info("Running ",  path.abspath(__file__), '...')

    # in_csv_path = Path("C:/p/productivity_calculator/inputs/Provider Productivity 10_16.csv")
    # in_csv_path = Path("C:/Users/Brandon/Downloads/Provider Productivity.csv")
    in_csv_path = Path("C:/Users/Brandon/Downloads/Provider Productivity 7_8-7_19.csv")
    out = get_total_units_by_date_by_provider_name_from_provider_productivity_csv_export(in_csv_path, facility_names = ["TP1"])

    logging.info("out:")
    pprint(out)
    logging.info("End of Main")


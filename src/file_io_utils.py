import csv
import json
from os.path import isfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

PATH_TYPES = Union[str, bytes, Path]

class CsvWriteFailedException(Exception):
    pass


def write_json(obj, json_path, indent = 4) -> None:
    """Overwrites if file exists"""
    Path(str(json_path)).parent.mkdir(exist_ok=True, parents=True)
    with open(json_path, "w") as f:
        json.dump(obj, f, indent=indent)


def read_json(json_path) -> Any:
    assert isfile(json_path), json_path
    return json.load(open(json_path, "r"))


def write_csv_from_row_dicts(row_dicts, csv_path, ordered_headers: Optional[List[str]]):
    # Build fieldname_dict_ordered (Dicts maintain insert order - Python 3.7+)
    fieldname_dict_ordered: dict = {}

    # Add ordered headers
    if ordered_headers:
        for header in ordered_headers:
            fieldname_dict_ordered[header] = None

    # Add all other "unordered" headers
    for row_dict in row_dicts:
        for key, _value in row_dict.items():
            fieldname_dict_ordered[key] = None

    # Write CSV
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(csv_path, "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=fieldname_dict_ordered.keys())
            dict_writer.writeheader()
            dict_writer.writerows(row_dicts)
    except PermissionError as e:
        raise CsvWriteFailedException(
            f"ERROR: Got PermissionError when trying to write {csv_path}, "
            "This is probably because the file is open in Excel. Close file and try again"
        ) from e


def read_csv_as_row_dicts(csv_path) -> List[Dict[str, str]]:
    """
    Reads csv file as a List of 'row-Dicts' (row_dicts)
        - The returned row_dicts will be a List with one element for each line.
        - Each element of this list will be a dictionary mapping the relevant 'Column Header' to the value in that
          column for the given row as a string

    Example:

    ```text
        As .csv:   >>   As Spreadsheet:   >>   As as returned "row_dicts":
        --------   >>   ---------------   >>   ------------------------
        Foo,Bar    >>   |Foo|Bar|         >>   [
        abc,123    >>   +---+---+         >>       {
        3.1,$%^    >>   |abc|123|         >>           'Foo': 'abc',
                   >>   +---+---+         >>           'Bar': '123'
                   >>   |3.1|$%^|         >>       },
                   >>                     >>       {
                   >>                     >>           'Foo': '3.1',
                   >>                     >>           'Bar': '$%^' 
                   >>                     >>       }
                   >>                     >>   ]
    ```
    """
    assert isfile(csv_path), csv_path
    return list(csv.DictReader(open(csv_path, "r", newline="", encoding="utf8"), dialect="excel"))



def read_lines_from_txt(filePath):
    with open(filePath) as textFile:  # May throw FileNotFoundError
        o =  list(l.rstrip() for l in textFile.readlines())
    textFile.close()
    return o
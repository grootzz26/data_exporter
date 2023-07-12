import datetime
import os
from collections import OrderedDict
from csv import DictWriter
from typing import List

import pandas
# import xlrd
from django.conf import settings
from django.db.models import QuerySet
from pandas import ExcelWriter
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
import secrets
import string
from .models import *


def random_n_token(n):
    """Generate a random string with numbers and characters with `n` length."""

    allowed_characters = (
        string.ascii_letters + string.digits
    )  # contains char and digits
    return "".join(secrets.choice(allowed_characters) for _ in range(n))


def exported_files_logs(source, excel_file_media_path):
    ExportDataLogs.objects.create(source=source, file_path=f"{settings.FILES_HOST}{excel_file_media_path}")


def write_list_of_dict_to_excel(
    data_list: List[dict], source=None
):
    """
    For the given data, generates an excel file. First writes a CSV file and then converts to XLSX.
    Based on the `is_temporary_file` param, the place of file creation varies. The output of this function is
    a public file url to the created file.

    Use Cases:
        1. Used in bulk upload output data files
        2. Bulk export from the frontend

    Note:
        1. This is used to write an excel file based on the given data.
        2. Multiple sheets can also be written using this function.
        3. This first writes the csv files and then converts the csv files to an excel file.

    Input Data Schema:
        [                                           ==> Excel file
            [                                       ==> Excel Sheet
                {                                   ==> Excel Sheet Row
                    "column_name_1": "value1",      ==> Row Column Data | Headers are got dynamically
                    "column_name_2": "value2",
                },
                ...
            ],
            ...
        ]

    Example Data Input:
        [
            [                                       ==> Sheet 1
                {"name":"Ajai Danial", "age": 12},      ==> Row 1
                {"name":"Danial", "age": 20},           ==> Row 2
            ],
            [                                       ==> Sheet 2
                {"name":"Ajai Danial", "age": 12},      ==> Row 1
                {"name":"Danial", "age": 20},           ==> Row 2
            ]
        ]
    """

    # decides where to create the file based on the `is_temporary_file`
    # if temporary, then the files are removed using a celery beat task
    # temporary files are generated for single time use and are not required after some time
    root_directory = settings.STORE_ROOT

    # config for the file
    file_name = random_n_token(10)
    excel_file_path = f"{root_directory}/{file_name}.xlsx"
    excel_file_media_path = f"{root_directory.split('/')[-1]}/{file_name}.xlsx"

    temp_csv_file_paths: List[str] = []
    for single_sheet_data_index in range(0, len(data_list)):
        single_sheet_data = data_list[single_sheet_data_index]
        csv_file_path = f"{root_directory}/{file_name}{single_sheet_data_index}.csv"

        # keys/header for the file | contains all the keys in the dictionaries
        dict_keys = []
        for data_dict in single_sheet_data:
            print(data_dict)
            dict_keys += [_ for _ in data_dict.keys() if _ not in dict_keys]

        # write csv
        with open(csv_file_path, "w") as outfile:
            writer = DictWriter(outfile, dict_keys)
            writer.writeheader()
            writer.writerows(single_sheet_data)

        # store for later conversion
        temp_csv_file_paths.append(csv_file_path)

    # write xlsx file
    writer = ExcelWriter(excel_file_path)

    for csv_path_index in range(0, len(temp_csv_file_paths)):
        csv_file_path = temp_csv_file_paths[csv_path_index]
        # read csv and write to excel
        read_file = pandas.read_csv(csv_file_path)
        read_file.to_excel(
            writer, index=None, header=True, sheet_name=f"sheet{csv_path_index + 1}"
        )
        # remove unnecessary files
        os.remove(csv_file_path)

    # save output
    writer.close()

    exported_files_logs(source, excel_file_media_path)

    return excel_file_media_path
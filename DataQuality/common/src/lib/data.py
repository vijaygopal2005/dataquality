import glob
import DataQuality.common.src.lib.common_dq_checks as dq
import os
import pandas as pd

home = os.path.expanduser("~")
path = f'{home}/dataquality/DataQuality/input_data'


def read_files_processed():
    files_processed = ''
    if os.path.isfile(path + "/files_processed.txt"):
        with open(path + "/files_processed.txt") as f:
            files_processed = f.readline()
    else:
        print("****files processed file does not exist*****")

    return files_processed


def read_input_data(dict_cols, files_processed):
    data = pd.DataFrame()
    for filename in glob.glob(path + "/*"):
        # Run Common DQ checks for each file read
        df, files_processed = dq.file_check(filename, dict_cols, files_processed)
        data = pd.concat([data, df], ignore_index=True)
        print("File Shape after concat--->", data.shape)
    return data, files_processed


def read_areas_blore(cols):
    # read areas in bangalore file
    df_areas_blore = pd.read_excel(path + '/Areas_in_blore.xlsx', dtype=cols)

    return df_areas_blore

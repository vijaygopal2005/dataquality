# This is a Python script that read csv files from location,checks for data quality and
# returns the clean and bad records.
import re
import pandas as pd
import os
import glob

files_processed = ''
all_data = pd.DataFrame()

def file_check(fname, data, dict_cols, files_processed):
    # check if file extension is csv and file is non-empty and if the file is already processed or not
    # and fname.split("/")[1] not in files_processed.split(",")
    if fname.endswith("csv") and os.path.getsize(fname):
        df = pd.read_csv(fname, usecols=list(dict_cols.keys()), dtype=dict_cols)
        data = pd.concat([data, df], ignore_index=True)
        if files_processed == '':
            files_processed = fname.split("/")[1]
        else:
            files_processed = files_processed + "," + fname.split("/")[1]
    return data, files_processed


def null_check(df, bad_rec, cols):
    df_clean_rec = pd.DataFrame()
    df_bad_rec = pd.DataFrame()

    for col in cols:
        df_clean_rec = pd.concat([df_clean_rec, df[df[col].notnull()]])
        df_bad_rec = pd.concat([df_bad_rec, df[df[col].isnull()]])

    bad_rec.loc[len(bad_rec.index)] = [df_bad_rec.index.to_list(), 'null']

    return df_clean_rec, bad_rec


def check_correctness(df, bad_rec, df_areas_blore):
    print("inside check")
    print(df.shape)

    df_check = df[df['location'].apply(lambda loc: df_areas_blore['Area'].str.contains(str(loc))).any(axis=1)]
    df_bad_rec = df[~df['location'].apply(lambda loc: df_areas_blore['Area'].str.contains(str(loc))).any(axis=1)]
    bad_rec.loc[len(bad_rec.index)] = [df_bad_rec.index.to_list(), 'location mismatch']

    return df_check,bad_rec


def dq_check(df):
    # print(df['phone'].head())
    bad_rec = pd.DataFrame(columns=['Row_num_list', 'Type_of_issue'])
    # remove special characters, commas from address
    df['address'] = df['address'].map(lambda x: re.sub(r'[^\w\s]', '', x))

    # handle phone numbers
    df['phone'] = df['phone'].str.replace("+", '', regex=True)
    df['phone'] = df['phone'].str.lstrip()
    df['phone'] = df['phone'].str.replace(" ", "-", regex=True)
    # split phone number by \r\n
    new = df['phone'].str.split("\r\n", expand=True)
    df['contact number 1'] = new[0]
    df['contact number 2'] = new[1]
    df.drop(columns=["phone"], inplace=True)

    df_clean_rec, bad_rec = null_check(df, bad_rec,
                                       ['name', 'contact number 1', 'contact number 2', 'location', 'dish_liked'])
    # print(df_null_rec)

    # read areas in bangalore file
    cols = {'Area': str, 'Taluk': str, 'District': str, 'State': str, 'Pincode': int}
    df_areas_blore = pd.read_excel('input_data/Areas_in_blore.xlsx', dtype=cols)
    df_loc_correctness = check_correctness(df_clean_rec, bad_rec, df_areas_blore)

    df_de_dups = df_loc_correctness[df_loc_correctness.duplicated() == False]
    df_dups = df_loc_correctness[df_loc_correctness.duplicated()].index.to_list()

    # bad_rec.at[1, 'Row_num_list'] = df_dups
    # bad_rec['Type_of_issue'] = 'duplicate'
    bad_rec.loc[len(bad_rec.index)] = [df_dups, 'duplicate']
    print(bad_rec)

    # writing clean records
    df_de_dups.to_csv('output_data/clean_records.out', index=False)
    bad_rec.to_csv('output_data/bad_records.bad', index=False)


if os.path.isfile("input_data/files_processed.txt"):
    with open("input_data/files_processed.txt") as f:
        files_processed = f.readline()

dict_cols = {'url': str, 'address': str, 'name': str, 'rate': str, 'votes': int, 'phone': str, 'location': str,
             'rest_type': str, 'dish_liked': object, 'cuisines': str, 'reviews_list': object}
for filename in glob.glob("input_data/*"):
    all_data, files_processed = file_check(filename, all_data, dict_cols, files_processed)

with open("input_data/files_processed.txt", 'w') as f:
    f.write(files_processed)

if all_data.empty:
    print("Files already processed")
else:
    dq_check(all_data)

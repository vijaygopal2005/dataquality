import pandas as pd
import os


def file_check(fname, dict_cols, files_processed):
    # check if file extension is csv and file is non-empty and if the file is already processed or not
    # and fname.split("/")[1] not in files_processed.split(",")
    df = pd.DataFrame()
    if fname.endswith("csv") and os.path.getsize(fname):
        print("reading file--->", fname)
        df = pd.read_csv(fname, usecols=list(dict_cols.keys()), dtype=dict_cols)
        print("File Shape--->", df.shape)
        if files_processed == '':
            files_processed = fname.split("/")[1]
        else:
            files_processed = files_processed + "," + fname.split("/")[1]

    return df, files_processed


def null_check(df, bad_rec, cols):
    df_bad_rec = pd.DataFrame()
    for col in cols:
        df_bad_rec = pd.concat([df_bad_rec, df[df[col].isnull()]])
        df = df[df[col].notnull()]

    bad_rec.loc[len(bad_rec.index)] = [df_bad_rec.index.to_list(), 'null']

    return df, bad_rec


def dedups(df, bad_rec):
    df_de_dups = df[df.duplicated() == False].copy()
    df_dups = df[df.duplicated()].index.to_list()

    bad_rec.loc[len(bad_rec.index)] = [df_dups, 'duplicate']

    return df_de_dups, bad_rec

import re


def remove_special_characters(df, cols):
    # remove special characters, commas from address
    for col in cols:
        df[col] = df[col].map(lambda x: re.sub(r'[^\w\s]', '', x))
    return df


def format_phone_nbr(df, cols):
    for col in cols:
        df[col] = df[col].str.replace("+", '', regex=True)
        df[col] = df[col].str.lstrip()
        df[col] = df[col].str.replace(" ", "-", regex=True)
        # split phone number by newline character
        new = df[col].str.split("\r\n", expand=True)
        df['contact number 1'] = new[0]
        df['contact number 2'] = new[1]
        df.drop(columns=["phone"], inplace=True)
    return df


def check_correctness(df, bad_rec, df_areas_blore):
    df_check = df[df['location'].apply(lambda loc: df_areas_blore['Area'].str.contains(str(loc))).any(axis=1)]
    df_bad_rec = df[~df['location'].apply(lambda loc: df_areas_blore['Area'].str.contains(str(loc))).any(axis=1)]
    bad_rec.loc[len(bad_rec.index)] = [df_bad_rec.index.to_list(), 'location mismatch']

    return df_check,bad_rec

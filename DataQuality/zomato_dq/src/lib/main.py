import DataQuality.common.src.lib.data as data
import DataQuality.zomato_dq.src.lib.dq_check as dq
import DataQuality.common.src.lib.common_dq_checks as common_dq
import pandas as pd
import os

home = os.path.expanduser("~")
inp_path = f'{home}/dataquality/DataQuality/zomato_dq/input_data'
out_path = f'{home}/dataquality/DataQuality/zomato_dq/output_data'


bad_rec = pd.DataFrame(columns=['Row_num_list', 'Type_of_issue'])

# Read files processed
files_processed = data.read_files_processed()
print(files_processed)
with open(inp_path+"/files_processed.txt", 'w') as f:
    f.write(files_processed)

# Read Input data
dict_cols = {'url': str, 'address': str, 'name': str, 'rate': str, 'votes': int, 'phone': str, 'location': str,
             'rest_type': str, 'dish_liked': object, 'cuisines': str, 'reviews_list': object}

all_data, files_processed = data.read_input_data(dict_cols, files_processed)
print("Shape of final data", all_data.shape)
print(all_data['phone'].head())

if ~all_data.empty:
    print("inside if")
    # Remove duplicates
    df,bad_rec = common_dq.dedups(all_data,bad_rec)
    print("shape after deduplication",df.shape)
    print("printing bad records", bad_rec)

    # calling function to remove special characters
    cols = ['address']
    df = dq.remove_special_characters(df, cols)
    print("Returning from Remove Special Character functon")
    print(df.shape)

    # check for null values
    cols = ['name','location','phone']
    df, bad_rec = common_dq.null_check(df, bad_rec, cols)
    print("Shape after removing null values", df.shape)
    print("printing bad records", bad_rec)

    # calling format phone numbers function
    cols = ['phone']
    df = dq.format_phone_nbr(df, cols)
    print("Returning from format phone number function")
    print(df.shape)


    # Read Areas in Bangalore file
    cols = {'Area': str, 'Taluk': str, 'District': str, 'State': str, 'Pincode': int}
    df_areas_blore = data.read_areas_blore(cols)
    print("Areas in Bangalore file shape", df_areas_blore.shape)

    # Check for location correctness against the Areas in Bangalore file
    df,bad_rec = dq.check_correctness(df, bad_rec, df_areas_blore)
    print("shape after location correctness",df.shape)
    print("printing bad records", bad_rec)

    # writing final outputs
    df.to_csv(out_path +'/clean_records.out', index=False)
    bad_rec.to_csv(out_path+'/bad_records.bad', index=False)


else:
    print("Files already processed or CSV files are not present or CSV files are empty")

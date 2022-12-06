import pandas as pd
import os
from DataQuality.zomato_dq.src.lib.dq_check import remove_special_characters,format_phone_nbr,check_correctness

home = os.path.expanduser("~")
inp_path = f'{home}/dataquality/DataQuality/zomato_dq/tests/input'
out_path = f'{home}/dataquality/DataQuality/zomato_dq/tests/output'

def test_remove_special_characters():

    # Read test input data
    df = pd.read_csv(inp_path+'/inp_special_char.csv')
    cols = ['col1','col2']
    out_df = remove_special_characters(df,cols)

    expected_df = pd.read_csv(out_path+'/out_special_char.csv')

    assert out_df.shape == expected_df.shape


def test_format_phone_nbr():

    # Read test input data
    df = pd.read_csv(inp_path + '/inp_phone_num.csv')
    cols = ['phone']
    out_df = format_phone_nbr(df,cols)

    expected_df = pd.read_csv(out_path+'/out_phone_num.csv')

    assert out_df.shape == expected_df.shape


def test_check_correctness():

    # Read test input data
    df = pd.read_csv(inp_path + '/inp_location_correctness.csv')
    df_areas = pd.read_csv(inp_path + '/inp_areas_blore.csv')
    bad_rec = pd.DataFrame(columns=['Row_num_list', 'Type_of_issue'])

    out_df,bad_rec = check_correctness(df,bad_rec,df_areas)
    print(out_df)
    print(bad_rec)
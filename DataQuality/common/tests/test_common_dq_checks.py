from DataQuality.common.src.lib.common_dq_checks import null_check, dedups
import os
import pandas as pd

home = os.path.expanduser("~")
inp_path = f'{home}/dataquality/DataQuality/common/tests/input'
out_path = f'{home}/dataquality/DataQuality/common/tests/output'



def test_null_check():
    # Read test input data
    df = pd.read_csv(inp_path + '/inp_null_check.csv')
    cols = ['col1','col2']
    bad_rec = pd.DataFrame(columns=['Row_num_list', 'Type_of_issue'])
    out_df,bad_rec = null_check(df,bad_rec, cols)

    expected_df = pd.read_csv(out_path + '/out_null_check.csv')

    assert out_df.shape == expected_df.shape

def test_dedups():
    # Read test input data
    df = pd.read_csv(inp_path + '/inp_dedups.csv')
    bad_rec = pd.DataFrame(columns=['Row_num_list', 'Type_of_issue'])
    out_df,bad_rec = dedups(df,bad_rec)
    print(out_df)

    expected_df = pd.read_csv(out_path + '/out_dedups.csv')

    assert out_df.shape == expected_df.shape

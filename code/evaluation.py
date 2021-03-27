import pandas as pd
import numpy as np
import argparse

def evaluate(user_file:str, base_file:str, cl_user_file:str=None, cl_base_file:str=None):
    '''calculates the unadjusted and adjusted robustness metrics'''
    
    user_df = pd.read_csv(user_file)
    base_df = pd.read_csv(base_file)
        
    assert user_df.shape==base_df.shape, f"DataFrame shapes {user_df.shape} and {base_df.shape} are incompatible"
    assert (user_df.columns==base_df.columns).any(), f"DataFrame column names or order is not matched"
    
    user_adj, base_adj = 0, 0
    if cl_user_file and cl_base_file:
        user_adj = pd.read_csv(cl_user_file)["clean"].item()
        base_adj = pd.read_csv(cl_base_file)["clean"].item()
    
    user_scores = np.array(user_df.iloc[0]) - user_adj
    base_scores = np.array(base_df.iloc[0]) - base_adj
    
    return {"unadjusted": np.mean(user_scores), "adjusted": np.mean(user_scores/base_scores)}

if __name__ == '__main__':
    
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-uf", "--user_file", type=str, required=True)
    parser.add_argument("-bf", "--base_file", type=str, required=True)
    parser.add_argument("-cluf", "--cl_user_file", type=str)
    parser.add_argument("-clbf", "--cl_base_file", type=str)

    # Read arguments from the command line
    args = parser.parse_args()
    
    # call function
    perf = evaluate(args.user_file, args.base_file, args.cl_user_file, args.cl_base_file)
    print(f"Unadjusted metric: {perf['unadjusted']*100:.2f}")
    print(f"Adjusted metric: {perf['adjusted']*100:.2f}")
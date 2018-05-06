"""
IO
=====

Provides high level functions to reading and writting data
"""
import pandas as pd

def convert_data_path_to_dataFrame(filepath, **kwargs):
    df = pd.read_csv(filepath, delim_whitespace=True, **kwargs)
    return df

def convert_data_path_to_dataFrame_3d(filepath):
    data_names = ['time', 'CFL', 
                  'pForceX', 'pForceY', 'pForceZ', 
                  'vForceX', 'vForceY', 'vForceZ']
    return convert_data_path_to_dataFrame(filepath, names=data_names)

def convert_data_path_to_dataFrame_2d(filepath):
    data_names = ['time', 'CFL', 
                  'pForceX', 'pForceY', 
                  'vForceX', 'vForceY']
    return convert_data_path_to_dataFrame(filepath, names=data_names)
"""
Signals
=====

Provides high level functions to processing Lift and Drag signals
"""
import pandas as pd
from statsmodels.robust.scale import mad as stats_mad

def calculate_total_forces(df):
    columns = df.columns.values
    pressure_forces = columns[['pForce' in c for c in columns]]
    viscous_forces = columns[['vForce' in c for c in columns]]
    total_forces = ['totalForce' + f[-1] for f in viscous_forces]
    
    for tf, pf, vf in zip(total_forces, pressure_forces, viscous_forces):
        df.loc[:,tf] = df[pf] + df[vf]
    return df

def calculate_signal_stats(df, column, signal_range=(0,1)):
    """
    signal_range - as ratios of the total time series
    """
    mn_signal, mx_signal = signal_range
    imn = round(len(df) * mn_signal)
    imx = round(len(df) * mx_signal)
    
    s_stat = df[column].iloc[imn:imx] #from DataFrame to Series
    mean = s_stat.mean()
    #mad = s_stat.mad()
    mad = stats_mad(s_stat.values) # MAD from Pandas does not give the expected results...:s
    return {'mean': mean, 'mad': mad, 'tmn': df['time'][imn], 'tmx': df['time'][imx]}
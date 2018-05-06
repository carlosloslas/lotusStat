#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developement file for lotsStat

Created on Sun May  6 11:23:56 2018

@author: closadalastra
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from statsmodels.robust.scale import mad as stats_mad


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

def plot_lift_signal(df, plot_stats=False, stats=None, show_stats=False, show_visc=False,**kwargs):
    fig = plt.figure(**kwargs)
    ax = plt.gca()
    df.plot('time', 'totalForceY', ax=ax)
    
    ax_y_mn, ax_y_mx = ax.get_ylim()
    ax_y_h = ax_y_mx - ax_y_mn
    ax_x_mn, ax_x_mx = ax.get_xlim()
    if show_visc:
        df.plot('time', 'vForceY', ax=ax)
    if plot_stats:
        #ax.axvline(stats['tmn'], color='gray', alpha=0.5)
        #ax.axvline(stats['tmx'], color='black', linewidth=1, alpha=0.5)
        ax.axhline(stats['mad'])
        
        ax_y_mn, ax_y_mx = ax.get_ylim()
        ax.add_patch(
            patches.Rectangle(
                (stats['tmn'], 1.15 * ax_y_mn),              # (x,y)
                stats['tmx'] - stats['tmn'],                          # width
                1.15 * ax_y_h,    # height
            alpha=0.25
            )   
        )
    if show_stats:
        ax.text(0.5 * (stats['tmn'] + stats['tmx']), 1.1*(df['totalForceY'].min()),
                'mad = {0}'.format(round(stats['mad'], 3)),
                horizontalalignment='center'
                )
        ax.set_ylim(1.05*ax_y_mn, ax_y_mx)
    return fig, ax

def plot_drag_signal(df, plot_stats=False, stats=None, show_stats=False, show_visc=False, **kwargs):
    fig = plt.figure(**kwargs)
    ax = plt.gca()
    df.plot('time', 'totalForceX', ax=ax)
    
    ax_y_mn, ax_y_mx = ax.get_ylim()
    ax_x_mn, ax_x_mx = ax.get_xlim()
    if show_visc:
        df.plot('time', 'vForceX', ax=ax)
    if plot_stats:
        #ax.axvline(stats['tmn'], color='black', linewidth=1)
        #ax.axvline(stats['tmx'], color='black', linewidth=1, alpha=0.5)
        ax.axhline(stats['mean'])
        
        ax.add_patch(
            patches.Rectangle(
                (stats['tmn'], ax_y_mn),              # (x,y)
                stats['tmx'] - stats['tmn'],                          # width
                ax_y_mx - ax_y_mn,    # height
            alpha=0.25
            )   
        )
    if show_stats:
        ax.text(0.5 * (stats['tmn'] + stats['tmx']), 0.45*(ax_y_mn + ax_y_mx),
                'mean = {0}'.format(round(stats['mean'], 3)),
                horizontalalignment='center'
                )
    return fig, ax

if __name__ == '__main__':
    data_path = './0.6/fort.9'
    
    data_df = convert_data_path_to_dataFrame_2d(data_path)
    data_df = data_df.iloc[500:,:]
    
    data_df = calculate_total_forces(data_df)
    
    lift_stats = calculate_signal_stats(data_df, 'totalForceY', signal_range=(0.8, 1))
    drag_stats = calculate_signal_stats(data_df, 'totalForceX', signal_range=(0.8, 1))
    
    fig, ax = plot_lift_signal(data_df, show_visc=True, plot_stats=True, stats=lift_stats, show_stats=True, figsize=(10,5))
    plot_drag_signal(data_df, plot_stats=True, stats=drag_stats, show_stats=True, figsize=(10,5))
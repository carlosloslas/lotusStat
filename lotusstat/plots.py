"""
Plots
=====

Provides high level functions to plotting routines
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_lift_signal(df, plot_stats=False, stats=None, show_visc=False,**kwargs):
    fig = plt.figure(**kwargs)
    ax = plt.gca()
    df.plot('time', 'totalForceY', ax=ax)
    if show_visc:
        df.plot('time', 'vForceY', ax=ax)
    if plot_stats:
        #ax.axvline(stats['tmn'], color='gray', alpha=0.5)
        #ax.axvline(stats['tmx'], color='black', linewidth=1, alpha=0.5)
        ax.axhline(stats['mad'])
        
        ax_y_mn, ax_y_mx = ax.get_ylim()
        ax.add_patch(
            patches.Rectangle(
                (stats['tmn'], ax_y_mn),              # (x,y)
                stats['tmx'] - stats['tmn'],                          # width
                ax_y_mx - ax_y_mn,    # height
            alpha=0.25
            )   
        )
        
    return fig, ax

def plot_drag_signal(df, plot_stats=False, stats=None, show_visc=False, **kwargs):
    fig = plt.figure(**kwargs)
    ax = plt.gca()
    df.plot('time', 'totalForceX', ax=ax)
    if show_visc:
        df.plot('time', 'vForceX', ax=ax)
    if plot_stats:
        #ax.axvline(stats['tmn'], color='black', linewidth=1)
        #ax.axvline(stats['tmx'], color='black', linewidth=1, alpha=0.5)
        ax.axhline(stats['mean'])
        
        ax_y_mn, ax_y_mx = ax.get_ylim()
        ax.add_patch(
            patches.Rectangle(
                (stats['tmn'], ax_y_mn),              # (x,y)
                stats['tmx'] - stats['tmn'],                          # width
                ax_y_mx - ax_y_mn,    # height
            alpha=0.25
            )   
        )
    return fig, ax
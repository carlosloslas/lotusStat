"""
Plots
=====

Provides high level functions to plotting routines
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.backends.backend_pdf as mpl_pdf

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

def save_figures_to_pdf(figures, filename):
    """
    Takes a list of figures and produces a PDF
    """
    with mpl_pdf.PdfPages(filename) as pdf:
        for fig in figures:
            pdf.savefig(fig)
    return None

def save_figures_to_pngs(figures_filenames):
    """
    List of pairs (figure, filename) to png figures
    """
    for fig, filename in figures_filenames:
        fig.savefig(filename)
    return None

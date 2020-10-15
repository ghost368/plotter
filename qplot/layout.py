import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.arraypad import _set_pad_area
import seaborn as sns
import plotly.express as px
import plotly.io
import pandas as pd

sns.set()  # set matplotlib settings to seaborn default
plotly.io.templates.default = 'seaborn'  # use plotly seaborn theme

MPL_CONFIG = {
    'default_fig_width': 10,
    'default_small_fig_width': 7,
    'unit_convertion_factor': 2,
    'default_height_units': 8,
    'default_number_cols': 1,
    'legend_font_size': 9,
    'axes_label_size': 12,
    'axes_title_size': 12,
}

PLOTLY_CONFIG = {
    'title_font_size': 16,
    'axes_title_size': 16,
    'axes_label_size': 14,
    'title_font_size': 18,
    'legend_font_size': 13,
    'legend_title_font_size': 13,
    'pixel_inch_convertion_factor': 90,
}


# tools
def get_mpl_axes(
    height=None,
    ncols=None,
    wide=False,
    wratios=None,
):
    """Get axes from plt.subplots with simpler interface and default settings

    Args:
        height (int, optional): Plot height in units. Defaults to _MPL_CONFIG['default_fig_width'].
        ncols (int, optional): Number of subplot columns. Defaults to _MPL_CONFIG['default_number_cols'].
        wide (bool, optional): If a wider plot should be used. Defaults to False.
        wratios (list-like, optional): Subplot width ratios, default will result in equal width. Defaults to None.
        return_fig (bool, optional): If the figure is returned together with the axes. Defaults to False.

    Returns:
        [tuple, ax]: tuple of axes, single ax, or (fig, axes tuple)
    """
    if height is None:
        height = MPL_CONFIG['default_height_units']
    if ncols is None:
        ncols = MPL_CONFIG['default_number_cols']
    figsize = [
        MPL_CONFIG['default_fig_width'],
        height / MPL_CONFIG['unit_convertion_factor'],
    ]
    if ncols == 1:
        if not wide:
            figsize[0] = MPL_CONFIG['default_small_fig_width']
    figsize = tuple(figsize)
    if wratios is not None:
        if len(wratios) != ncols:
            raise ValueError(
                'Width ratios must be the same length as the number of subplots'
            )
        gridspec_kw = {'width_ratios': list(wratios)}
    else:
        gridspec_kw = None
    fig, axes = plt.subplots(1, ncols, figsize=figsize, gridspec_kw=gridspec_kw)
    if not isinstance(axes, np.ndarray):
        axes = np.array([axes])
    return fig, axes


def set_mpl_layout(
    ax,
    title=None,
    xlabel=None,
    ylabel=None,
    legend=True,
    legend_outside=True,
    legend_labels=None,
    **kwargs,
):
    """Wrapper to specify certain layout properties for mpl subplots

    Args:
        ax ([ax]): matplotlib axis
        title (str, optional): Title. Defaults to None.
        xlabel (str, optional): X-label name. Defaults to None.
        ylabel (str, optional): Y-label name. Defaults to None.
        legend (bool, optional): If the legend is shown. Defaults to True.
        legend_outside (bool, optional): If the legend is located outside the plot. Defaults to True.
    """
    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if legend:
        legend_kwargs = {}
        if legend_outside:
            legend_kwargs['bbox_to_anchor'] = (1, 1)
            legend_kwargs['loc'] = 'upper left'
        if legend_labels is not None:
            legend_kwargs['labels'] = legend_labels
        ax.legend(**legend_kwargs)
    plt.tight_layout()


def set_plotly_layout(
    fig,
    height=None,
    title=None,
    xlabel=None,
    ylabel=None,
    legend=True,
    wide=False,
    is_svg=False,
    legend_label_map=None,
    **kwargs,
):
    """Simple interface for modifying the layout of plotly plot

    Args:
        fig ([figure]): Figure to modify
        height (int, optional): Height in units. Defaults to 8.
        title (str, optional): Title. Defaults to None.
        xlabel (str, optional): X-label name. Defaults to None.
        ylabel (str, optional): Y-label name. Defaults to None.
        legend (bool, optional): If the legend is show. Defaults to True.
        wide (bool, optional): If larger plot width is used. Defaults to False.
        is_svg (bool, optional): If static svg renderer is used - will result in no interactivity, but
                can be exported with nbconvert to pdf. Defaults to False.
        legend_label_map ([dict-like], optional): Mapping to modify legend names, absent names will remain the
                same. Defaults to None.
    """
    if height is None:
        height = MPL_CONFIG['default_height_units']
    fig.update_layout(
        xaxis_title_font_size=PLOTLY_CONFIG['title_font_size'],
        yaxis_title_font_size=PLOTLY_CONFIG['title_font_size'],
        yaxis_tickfont_size=PLOTLY_CONFIG['axes_label_size'],
        xaxis_tickfont_size=PLOTLY_CONFIG['axes_label_size'],
        title_font_size=PLOTLY_CONFIG['title_font_size'],
        legend_font_size=PLOTLY_CONFIG['legend_font_size'],
        legend_title_font_size=PLOTLY_CONFIG['legend_title_font_size'],
    )
    if title is not None:
        fig.update_layout(title=title)
    if xlabel is not None:
        fig.update_layout(xaxis_title_text=xlabel)
    if ylabel is not None:
        fig.update_layout(yaxis_title_text=ylabel)
    fig.update_layout(showlegend=legend)
    width = (
        MPL_CONFIG['default_fig_width'] * PLOTLY_CONFIG['pixel_inch_convertion_factor']
        if wide
        else MPL_CONFIG['default_small_fig_width']
        * PLOTLY_CONFIG['pixel_inch_convertion_factor']
    )
    height = int(
        PLOTLY_CONFIG['pixel_inch_convertion_factor']
        * height
        / MPL_CONFIG['unit_convertion_factor']
    )
    if legend_label_map is not None:
        assert isinstance(legend_label_map, dict), 'Legend label map must be a dict'
        for fd in fig.data:
            if fd['name'] in legend_label_map:
                fd['name'] = legend_label_map[fd['name']]
    if not is_svg:
        fig.update_layout(width=width, height=height)
    else:
        # is svg renderer is chose the figure will be shown automatically
        fig.show(width=width, height=height, renderer='svg')

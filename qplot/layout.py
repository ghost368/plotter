import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Tuple

from .types import Axis, FigureMpl, FigurePlotly

MPL_CONFIG = {
    'default_fig_width': 10,
    'default_small_fig_width': 7,
    'unit_convertion_factor': 2,
    'default_height_units': 7,
    'default_number_cols': 1,
    'legend_font_size': 9,
    'axes_label_size': 12,
    'axes_title_size': 12,
}

PLOTLY_CONFIG = {
    'title_font_size': 16,
    'axes_title_size': 16,
    'axes_label_size': 16,
    'title_font_size': 18,
    'unit_convertion_factor': 1.5,
    'legend_font_size': 14,
    'legend_title_font_size': 14,
    'pixel_inch_convertion_factor': 90,
}


def generate_mpl_figure(
    height: int = None,
    ncols: int = None,
    wide: bool = False,
    wratios: List[float] = None,
) -> Tuple[FigureMpl, List[Axis]]:
    """Get axes from plt.subplots with simpler interface and default settings

    Args:
        height (int, optional): Plot height in units
        ncols (int, optional): Number of subplot columns
        wide (bool, optional): If a wider plot should be used
        wratios (list-like, optional): Subplot width ratios, default will result in equal width

    Returns:
        tuple: tuple of a figure and a list of axes
    """
    if height is None:
        height = MPL_CONFIG['default_height_units']
    if ncols is None:
        ncols = MPL_CONFIG['default_number_cols']

    # specify figsize
    figsize = [
        MPL_CONFIG['default_fig_width'],
        height / MPL_CONFIG['unit_convertion_factor'],
    ]
    if ncols == 1:
        if not wide:
            figsize[0] = MPL_CONFIG['default_small_fig_width']
    figsize = tuple(figsize)

    # specify width ratios
    if wratios is not None:
        if len(wratios) != ncols:
            raise ValueError(
                'Width ratios must be the same length as the number of subplots'
            )
        gridspec_kw = {'width_ratios': list(wratios)}
    else:
        gridspec_kw = None

    fig, axes = plt.subplots(1, ncols, figsize=figsize, gridspec_kw=gridspec_kw)

    # plt.subplots return ndarray of axes if more than 1
    if not isinstance(axes, np.ndarray):
        axes = np.array([axes])
    axes = list(axes)
    return fig, axes


def set_mpl_layout(
    ax: Axis,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    legend: bool = True,
    legend_outside: bool = True,
    legend_labels: List[str] = None,
    **kwargs,
):
    """Wrapper to specify certain layout properties for mpl subplots

    Args:
        ax (Axis): matplotlib axis
        title (str, optional): Title
        xlabel (str, optional): X-label name
        ylabel (str, optional): Y-label name
        legend (bool, optional): If the legend is shown
        legend_outside (bool, optional): If the legend is located outside the plot
    """
    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    set_ax_legend(ax, legend, legend_outside, legend_labels)
    plt.tight_layout()


def set_ax_legend(
    ax: Axis,
    legend: bool = True,
    legend_outside: bool = True,
    legend_labels: List[str] = None,
):
    if legend:
        legend_kwargs = {}
        if legend_outside:
            legend_kwargs['bbox_to_anchor'] = (1, 1)
            legend_kwargs['loc'] = 'upper left'
        if legend_labels is not None:
            legend_kwargs['labels'] = legend_labels
        ax.legend(**legend_kwargs)
    else:
        leg = ax.get_legend()
        if leg is not None:
            leg.remove()  # legend = False can also be used


def set_plotly_layout(
    fig: FigurePlotly,
    height: int = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    legend: bool = True,
    wide: bool = False,
    is_svg: bool = False,
    legend_label_map: dict = None,
    **kwargs,
):
    """Simple interface for modifying the layout of plotly plot

    Args:
        fig (FigurePlotly): Figure to modify
        height (int, optional): Height in units
        title (str, optional): Title
        xlabel (str, optional): X-label name
        ylabel (str, optional): Y-label name
        legend (bool, optional): If the legend is show
        wide (bool, optional): If larger plot width is used
        is_svg (bool, optional): If static svg renderer is used - will result in no interactivity, but
                can be exported with nbconvert to pdf. Defaults to False.
        legend_label_map ([dict-like], optional): Mapping to modify legend names, absent names will remain the
                same
    """
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

    # adjusting legend
    fig.update_layout(showlegend=legend)
    if legend:
        if legend_label_map is not None:
            assert isinstance(legend_label_map, dict), 'Legend label map must be a dict'
            for fd in fig.data:
                if fd['name'] in legend_label_map:
                    fd['name'] = legend_label_map[fd['name']]

    # specifying width and height
    width = (
        MPL_CONFIG['default_fig_width'] * PLOTLY_CONFIG['pixel_inch_convertion_factor']
        if wide
        else MPL_CONFIG['default_small_fig_width']
        * PLOTLY_CONFIG['pixel_inch_convertion_factor']
    )
    if height is None:
        height = MPL_CONFIG['default_height_units']
    height = int(
        PLOTLY_CONFIG['pixel_inch_convertion_factor']
        * height
        / PLOTLY_CONFIG['unit_convertion_factor']
    )
    if not is_svg:
        fig.update_layout(width=width, height=height)
    else:
        # is svg renderer is chose the figure will be shown automatically
        fig.show(width=width, height=height, renderer='svg')

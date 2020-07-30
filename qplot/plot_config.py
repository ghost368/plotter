import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io
import pylab

sns.set()  # set matplotlib settings to seaborn default
plotly.io.templates.default = 'seaborn'  # use plotly seaborn theme

_MPL_CONFIG = {
    'default_fig_width': 10,
    'default_small_fig_width': 7,
    'unit_convertion_factor': 2,
    'default_height_units': 8,
    'default_number_cols': 1,
    'legend_font_size': 9,
    'axes_label_size': 12,
    'axes_title_size': 12,
}

_PLOTLY_CONFIG = {
    'title_font_size': 16,
    'axes_title_size': 16,
    'axes_label_size': 14,
    'title_font_size': 18,
    'legend_font_size': 13,
    'legend_title_font_size': 13,
    'pixel_inch_convertion_factor': 90,
}


# tools
def get_axes(
    height=_MPL_CONFIG['default_fig_width'],
    ncols=_MPL_CONFIG['default_number_cols'],
    small=False,
    wratios=None,
    return_fig=False,
):
    """Get axes from plt.subplots with simpler interface and default settings

    Args:
        height (int, optional): Plot height in units. Defaults to _MPL_CONFIG['default_fig_width'].
        ncols (int, optional): Number of subplot columns. Defaults to _MPL_CONFIG['default_number_cols'].
        small (bool, optional): If a more narrow plot should be used. Defaults to False.
        wratios (list-like, optional): Subplot width ratios, default will result in equal width. Defaults to None.
        return_fig (bool, optional): If the figure is returned together with the axes. Defaults to False.

    Returns:
        [tuple, ax]: tuple of axes, single ax, or (fig, axes tuple)
    """
    figsize = [
        _MPL_CONFIG['default_fig_width'],
        height / _MPL_CONFIG['unit_convertion_factor'],
    ]
    if ncols == 1:
        if small:
            figsize[0] = _MPL_CONFIG['default_small_fig_width']
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
    if return_fig:
        return fig, axes
    else:
        return axes


def set_mpl_layout(
    ax, title=None, xlabel=None, ylabel=None, legend=True, legend_outside=True
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
        if legend_outside:
            ax.legend(bbox_to_anchor=(1, 1), loc='upper left')
        else:
            ax.legend()
    plt.tight_layout()


def set_pd_backend(backend='matplotlib'):
    """Simple function to set pandas plotting backend

    Args:
        backend (str, optional): Backend name. Defaults to 'matplotlib'.
    """
    pd.options.plotting.backend = backend


def set_plotly_layout(
    fig,
    height=8,
    title=None,
    xlabel=None,
    ylabel=None,
    legend=True,
    small=False,
    is_svg=False,
    legend_label_map=None,
):
    """Simple interface for modifying the layout of plotly plot

    Args:
        fig ([figure]): Figure to modify
        height (int, optional): Height in units. Defaults to 8.
        title (str, optional): Title. Defaults to None.
        xlabel (str, optional): X-label name. Defaults to None.
        ylabel (str, optional): Y-label name. Defaults to None.
        legend (bool, optional): If the legend is show. Defaults to True.
        small (bool, optional): If smaller plot width is used. Defaults to False.
        is_svg (bool, optional): If static svg renderer is used - will result in no interactivity, but 
                can be exported with nbconvert to pdf. Defaults to False.
        legend_label_map ([dict-like], optional): Mapping to modify legend names, absent names will remain the 
                same. Defaults to None.
    """
    fig.update_layout(
        xaxis_title_font_size=_PLOTLY_CONFIG['title_font_size'],
        yaxis_title_font_size=_PLOTLY_CONFIG['title_font_size'],
        yaxis_tickfont_size=_PLOTLY_CONFIG['axes_label_size'],
        xaxis_tickfont_size=_PLOTLY_CONFIG['axes_label_size'],
        title_font_size=_PLOTLY_CONFIG['title_font_size'],
        legend_font_size=_PLOTLY_CONFIG['legend_font_size'],
        legend_title_font_size=_PLOTLY_CONFIG['legend_title_font_size'],
    )
    fig.update_layout(
        title=title, xaxis_title_text=xlabel, yaxis_title_text=ylabel, showlegend=legend
    )
    width = (
        _MPL_CONFIG['default_fig_width']
        * _PLOTLY_CONFIG['pixel_inch_convertion_factor']
        if not small
        else _MPL_CONFIG['default_small_fig_width']
        * _PLOTLY_CONFIG['pixel_inch_convertion_factor']
    )
    height = int(
        _PLOTLY_CONFIG['pixel_inch_convertion_factor']
        * height
        / _MPL_CONFIG['unit_convertion_factor']
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

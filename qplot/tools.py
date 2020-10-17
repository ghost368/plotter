import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from dataclasses import dataclass
from typing import Tuple, Callable
from dataclasses import dataclass

__all__ = ['stem_plot', 'plot_func', 'align_ticks', 'BarAnnotator']


def stem_plot(
    x,
    y,
    ax=None,
    marker='o',
    marker_color='b',
    marker_size=5,
    base_color='r',
    base_lw=1,
    stem_color='grey',
    stem_lw=1,
):
    if ax is None:
        ax = plt.gca()
    markerline, stemlines, baseline = ax.stem(x, y, label='values')
    plt.setp(baseline, color=base_color, linewidth=base_lw)
    plt.setp(stemlines, color=stem_color, linewidth=stem_lw)
    plt.setp(markerline, marker=marker, color=marker_color, markersize=marker_size)


def plot_func(func, ax, n_points=1000):
    func = np.vectorize(func)
    xvals = np.linspace(*ax.get_xlim(), n_points)
    ax.plot(xvals, func(xvals))


def align_ticks(ax1, ax2):
    llim = ax1.get_ylim()
    rlim = ax2.get_ylim()
    tick_mapper = lambda x: rlim[0] + (x - llim[0]) / (llim[1] - llim[0]) * (
        rlim[1] - rlim[0]
    )
    ax2.yaxis.set_major_locator(mpl.ticker.FixedLocator(tick_mapper(ax1.get_yticks())))
    ax2.grid(None)


# bar annotation tool
Patch = mpl.patches.Patch
PosVal = Tuple[float, Tuple[float, float]]
Axis = mpl.axes.Axes
PosValFunc = Callable[[Patch], PosVal]


@dataclass  # use dataclass to autogenerate __init__ method
class BarAnnotator:
    font_size: int = 10
    color: str = 'k'
    n_decim: int = 2

    # vertical bar plot annotation
    def annotate(self, ax: Axis, centered: bool = False):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_height()
            div = 2 if centered else 1
            pos = (p.get_x() + p.get_width() / 2, p.get_y() + p.get_height() / div)
            return value, pos

        va = 'center' if centered else 'bottom'
        self._annotate(ax, get_vals, ha='center', va=va)

    # horizontal bar plot annotation
    def annotate_hor(self, ax: Axis, centered=False):
        def get_vals(p: Patch) -> PosVal:
            value = p.get_width()
            div = 2 if centered else 1
            pos = (
                p.get_x() + p.get_width() / div,
                p.get_y() + p.get_height() / 2,
            )
            return value, pos

        ha = 'center' if centered else 'left'
        self._annotate(ax, get_vals, ha=ha, va='center')

    def _annotate(self, ax, func: PosValFunc, **kwargs):
        cfg = {'color': self.color, 'fontsize': self.font_size, **kwargs}
        for p in ax.patches:
            value, pos = func(p)
            ax.annotate(f'{value:.{self.n_decim}f}', pos, **cfg)
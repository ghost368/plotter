import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from dataclasses import dataclass
from typing import Tuple, Callable
from collections.abc import Sequence
from dataclasses import dataclass

from .types import Axis, Patch

PosVal = Tuple[float, Tuple[float, float]]

__all__ = ['Stem', 'plot_func', 'align_ticks', 'BarAnnotator']


# use class instead of function to avoid repeating the step plot specifications
@dataclass
class Stem:
    """ Class for configuring stem plots """

    marker: str = 'o'
    marker_color: str = 'b'
    marker_size: int = 5
    base_color: str = 'r'
    base_lw: int = 1
    stem_color: str = 'grey'
    stem_lw: int = 1

    def plot(
        self,
        x: Sequence,
        y: Sequence,
        ax: Axis = None,
    ):
        """ Make stem plot """
        if ax is None:
            ax = plt.gca()  # default to current active axis
        markerline, stemlines, baseline = ax.stem(x, y, label='values')
        plt.setp(baseline, color=self.base_color, linewidth=self.base_lw)
        plt.setp(stemlines, color=self.stem_color, linewidth=self.stem_lw)
        plt.setp(
            markerline,
            marker=self.marker,
            color=self.marker_color,
            markersize=self.marker_size,
        )


@dataclass  # use dataclass to autogenerate __init__ method
class BarAnnotator:
    """ Class for annotating bar plots with values """

    font_size: int = 10
    color: str = 'black'
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

    def _annotate(self, ax, func: Callable, **kwargs):
        cfg = {'color': self.color, 'fontsize': self.font_size, **kwargs}
        for p in ax.patches:
            value, pos = func(p)
            ax.annotate(f'{value:.{self.n_decim}f}', pos, **cfg)


def plot_func(func: Callable, ax: Axis, n_xvalues: int = 1000):
    """ Plot function on a given axis for the current axis limits range """
    func = np.vectorize(func)
    xvals = np.linspace(*ax.get_xlim(), n_xvalues)
    ax.plot(xvals, func(xvals))


def align_ticks(ax1: Axis, ax2: Axis):
    """ Align y-ticks on ax2 with the ticks on ax1, allows to have common grid """
    lim_ax1 = ax1.get_ylim()
    lim_ax2 = ax2.get_ylim()
    tick_mapper = lambda x: lim_ax2[0] + (x - lim_ax1[0]) / (
        lim_ax1[1] - lim_ax1[0]
    ) * (lim_ax2[1] - lim_ax2[0])
    ax2.yaxis.set_major_locator(mpl.ticker.FixedLocator(tick_mapper(ax1.get_yticks())))
    ax2.grid(None)
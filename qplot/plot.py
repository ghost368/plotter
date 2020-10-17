from contextlib import contextmanager
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import typing
import numpy as np

from .layout import set_plotly_layout, set_mpl_layout, get_mpl_axes
from . import tools

Engine = typing.Literal['matplotlib', 'plotly']


class Plot:
    def __init__(self, fig=None, axes=None, engine: Engine = 'matplotlib'):
        self.fig = fig
        self._axes = axes
        if engine not in ['matplotlib', 'plotly']:
            raise ValueError(f"engine must belong to {typing.get_args(Engine)}")
        self._engine = engine

    def ax(self, idx=1):
        return self._axes[idx - 1]

    def nplots(self):
        if self._axes is None:
            return 1
        return len(self._axes)

    def set_layout(self, ax_idx=None, **kwargs):
        if self._engine == 'matplotlib':
            if ax_idx is None:
                ax_idx = 1
            set_mpl_layout(ax=self.ax(ax_idx), **kwargs)
        else:
            set_plotly_layout(fig=self.fig, **kwargs)

    def add_ax(self, new_ax):
        self._axes = np.append(self._axes, new_ax)


@contextmanager
def plot(
    height=None,
    ncols=None,
    wratios=None,
    wide=False,
    engine: Engine = 'matplotlib',
    twin_ax=False,
    align_ticks=True,
    lcolor='b',
    rcolor='r',
    **kwargs,
):
    if engine == 'matplotlib':
        fig, axes = get_mpl_axes(height=height, ncols=ncols, wratios=wratios, wide=wide)
        p = Plot(fig, axes, engine=engine)
        if p.nplots() == 1:
            plt.sca(p.ax())
        if twin_ax:
            p.add_ax(p.ax().twinx())
    elif engine == 'plotly':
        p = Plot(engine=engine)
        pd.options.plotting.backend = 'plotly'
    else:
        raise ValueError(f'engine must belong to {typing.get_args(Engine)}')

    try:
        yield p
    finally:
        if p.nplots() == 1:
            p.set_layout(wide=wide, height=height, **kwargs)
        if twin_ax:
            # align ticks for left and right plots to have consistent common grid
            if align_ticks:
                tools.align_ticks(p.ax(1), p.ax(2))

            # adding colors to ticks and labels
            p.ax(1).tick_params(axis='y', labelcolor=rcolor, color=rcolor)
            p.ax(2).tick_params(axis='y', labelcolor=lcolor, color=lcolor)

        if engine == 'plotly':
            p.fig.show()
        pd.options.plotting.backend = 'matplotlib'

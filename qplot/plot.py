from contextlib import contextmanager
import pandas as pd
import matplotlib.pyplot as plt
import typing

from .layout import set_plotly_layout, set_mpl_layout, get_mpl_axes

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


@contextmanager
def plot(
    height=None,
    ncols=None,
    wratios=None,
    wide=False,
    engine: Engine = 'matplotlib',
    **kwargs,
):
    if engine == 'matplotlib':
        fig, axes = get_mpl_axes(height=height, ncols=ncols, wratios=wratios, wide=wide)
        pt = Plot(fig, axes, engine=engine)
        if pt.nplots() == 1:
            plt.sca(pt.ax())
    elif engine == 'plotly':
        pt = Plot(engine=engine)
        pd.options.plotting.backend = 'plotly'
    else:
        raise ValueError(f'engine must belong to {typing.get_args(Engine)}')

    try:
        yield pt
    finally:
        if pt.nplots() == 1:
            pt.set_layout(wide=wide, height=height, **kwargs)
        if engine == 'plotly':
            pt.fig.show()
        pd.options.plotting.backend = 'matplotlib'
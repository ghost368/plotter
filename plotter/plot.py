from contextlib import contextmanager
from qplot.layout import set_ax_legend
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from dataclasses import dataclass

from . import tools, layout

from typing import List
import typing

from .types import Figure, FigurePlotly, FigureMpl, Engine, Axis


@dataclass
class Plot:
    _fig: Figure = None
    _axes: List[Axis] = None
    engine: str = 'matplotlib'

    def __post_init__(self):
        """ Check engine value """
        if self.engine not in ['matplotlib', 'plotly']:
            raise ValueError(f"engine must belong to {typing.get_args(Engine)}")

    def ax(self, idx: int = 1):
        """ Get axis, index starting from 1 """
        return self._axes[idx - 1]

    def nsubplots(self):
        """ Get the number of subplots """
        if self._axes is None:
            return 1
        return len(self._axes)

    def set_layout(self, ax_idx: int = 1, **kwargs):
        """Set axis layout

        Args:
            ax_idx (int, optional):  axis index
        """
        if self.engine == 'matplotlib':
            layout.set_mpl_layout(ax=self.ax(ax_idx), **kwargs)
        else:
            layout.set_plotly_layout(fig=self._fig, **kwargs)

    def add_ax(self, new_ax: Axis):
        """ Add new axis to the axes list """
        self._axes = self._axes + [new_ax]

    def set_fig(self, fig: FigurePlotly):
        if self.engine != 'plotly':
            raise NotImplementedError(
                'Setting figure is only available for plotly engine'
            )
        self._fig = fig

    def has_fig(self):
        if self.engine == 'plotly':
            return isinstance(self._fig, FigurePlotly)
        else:
            return isinstance(self._fig, FigureMpl)

    def tight_layout(self):
        if self.has_fig() and self.engine == 'matplotlib':
            self._fig.tight_layout()


@contextmanager
def plot(
    height=None,
    ncols=None,
    wratios=None,
    wide=False,
    default_layout=True,
    engine: Engine = 'matplotlib',
    twin_ax: bool = False,
    align_ticks: bool = True,
    lcolor: str = 'b',
    rcolor: str = 'r',
    legend: bool = None,
    legend_outside: bool = True,
    **kwargs,
):
    if engine == 'matplotlib':
        fig, axes = layout.generate_mpl_figure(
            height=height, ncols=ncols, wratios=wratios, wide=wide
        )
        plot_ = Plot(fig, axes, 'matplotlib')

        # if single axis, set current plt axis to it
        if plot_.nsubplots() == 1:
            plt.sca(plot_.ax())

        # twin ax with double y range
        if twin_ax:
            if plot_.nsubplots() > 1:
                raise ValueError('Twin ax is only available for a single subplot')
            plot_.add_ax(plot_.ax().twinx())
    else:
        plot_ = Plot(engine='plotly')
        pd.options.plotting.backend = 'plotly'

    try:
        yield plot_
    finally:
        if legend is None:
            # default is True except when we have twinx ax (requires manual setup)
            legend = False if twin_ax else True

        if plot_.engine == 'plotly':
            if not plot_.has_fig():
                raise ValueError('Must set figure for a plotly graph')

        # set layout using the context manager args if unique ax and default_layout is True
        # otherwise layout for each ax must be set separately using plot_.set_layout
        if plot_.nsubplots() == 1:
            if default_layout:
                plot_.set_layout(
                    wide=wide,
                    height=height,
                    legend=legend,
                    legend_outside=legend_outside,
                    **kwargs,
                )

        if plot_.nsubplots() > 1:
            if legend:
                for i in range(1, plot_.nsubplots() + 1):
                    layout.set_ax_legend(
                        plot_.ax(i), legend=True, legend_outside=legend_outside
                    )

        # processing twix axis
        if twin_ax:
            # align ticks for left and right plots to have consistent common grid
            if align_ticks:
                tools.align_ticks(plot_.ax(1), plot_.ax(2))

            # adding colors to ticks and labels
            plot_.ax(1).tick_params(axis='y', labelcolor=rcolor, color=rcolor)
            plot_.ax(2).tick_params(axis='y', labelcolor=lcolor, color=lcolor)

        plot_.tight_layout()

        # post serve for plotly
        if engine == 'plotly':
            plot_._fig.show()
            pd.options.plotting.backend = 'matplotlib'

import numpy as np
import pytest
import plotly.express as px

from qplot import get_axes, set_mpl_layout, set_plotly_layout


def test_activate():
    from qplot import activate


def test_mpl():
    data = np.random.rand(20, 2) 
    ax1, ax2 = get_axes(height=10, ncols=2, wratios=[2, 3])
    ax1.plot(data)
    ax2.scatter(range(len(data)), data[:, 0])
    set_mpl_layout(ax1, 'title', 'xvalues', 'yvalues', legend_outside=False)

    fig, ax = get_axes(return_fig=True)
    ax.plot(data)
    set_mpl_layout(ax, legend=False)

    with pytest.raises(ValueError):
        axes = get_axes(ncols=3, wratios=[1, 2])    



def test_plotly():
    data = np.random.rand(20, 2) 
    fig = px.line(x=range(len(data)), y=data[:, 0])
    set_plotly_layout(fig, height=8, title='title', ylabel='y values', small=True)
    fig.show()

    fig = px.line(x=range(len(data)), y=data[:, 1])
    set_plotly_layout(fig, is_svg=True)
    fig.show()

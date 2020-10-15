from matplotlib.pyplot import legend
import numpy as np
import pandas as pd
import pytest
import plotly.express as px

import qplot


def test_activate():
    from qplot import activate


def test_mpl():
    data = np.random.rand(20, 2)

    with qplot.plot(6, title='some title', wide=True, legend=False) as p:
        p.ax().plot(data)

    with pytest.raises(ValueError):
        with qplot.plot(ncols=3, wratios=[1, 2]) as p:
            p.ax().plot(data)

    df = pd.DataFrame(data)
    with qplot.plot(xlabel='x'):
        df.plot()

    with qplot.plot(ncols=2, wratios=[2, 1]) as p:
        df.plot(ax=p.ax(1))
        df.plot(ax=p.ax(2))
        p.set_layout(ax_idx=1, title='first')
        p.set_layout(ax_idx=2, ylabel='y 2')


def test_plotly():
    data = np.random.rand(20, 2)

    with qplot.plot(wide=True, engine='plotly', title='title') as p:
        p.fig = px.line(x=range(len(data)), y=data[:, 0])

    df = pd.DataFrame(data)
    with qplot.plot(engine='plotly') as p:
        p.fig = df.plot()

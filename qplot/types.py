import matplotlib as mpl
import plotly
from typing import Literal, Union

# create separate types module
Engine = Literal['matplotlib', 'plotly']
FigureMpl = mpl.figure.Figure
Axis = mpl.axes.Axes
FigurePlotly = plotly.graph_objects.Figure
Figure = Union[FigurePlotly, FigureMpl]
Patch = mpl.patches.Patch

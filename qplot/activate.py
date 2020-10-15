import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io
import pylab
from loguru import logger

from IPython import get_ipython

from .layout import MPL_CONFIG


sns.set()  # set matplotlib settings to seaborn default
plotly.io.templates.default = 'seaborn'  # use plotly seaborn theme

params = {
    'legend.fontsize': MPL_CONFIG['legend_font_size'],
    'axes.labelsize': MPL_CONFIG['axes_label_size'],
    'axes.titlesize': MPL_CONFIG['axes_title_size'],
}
plt.rcParams.update(params)

ipython = get_ipython()
# If in ipython, load autoreload extension
if ipython is not None:
    logger.info('IPython detected, applying inline plotting and svg figure format.')
    ipython.magic(
        "config InlineBackend.figure_format = 'svg'"
    )  # use svg image output format in jupyter
    ipython.magic('matplotlib inline')  # inline jupyter plots
else:
    logger.info('No IPython detected. Magic commands were ignored.')

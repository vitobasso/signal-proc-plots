__author__ = 'victor'

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# slider layout
left = .25
bottom = .05
height = .03
width = .65
slspace = .05
margin = .04


# util functions
def _param_init(param):
    return param['min'] + float(param['max'] - param['min']) / 2


def _slider_val(slider):
    return slider.val


def _create_slider(param, i):
    axes = plt.axes([left, bottom + i*slspace, width, height])
    return Slider(axes, param['name'], param['min'], param['max'], valinit=_param_init(param))


class Plot:

    def __init__(self, functions, tmin=0, tmax=1, tstep=0.001, ymin=-10, ymax=10):
        self.tmin = tmin
        self.tmax = tmax
        self.ymin = ymin
        self.ymax = ymax
        self.t = np.arange(tmin, tmax, tstep)
        self.functions = functions

    def _setup_sliders(self):
        i = 0
        for fun_dict in self.functions:
            sliders = []
            for param in fun_dict['params']:
                i += 1
                sliders.append(_create_slider(param, i))
            fun_dict['sliders'] = sliders

        def update(val):

            x = self.t
            for fun_dict in self.functions:
                fun = fun_dict['fun']
                plot = fun_dict['plot']
                sliders = fun_dict['sliders']

                values = map(_slider_val, sliders)
                y = fun(x, *values)
                plot.set_ydata(y)
                self.fig.canvas.draw_idle()
                x = y

        for fun_dict in self.functions:
            sliders = fun_dict['sliders']
            for s in sliders:
                s.on_changed(update)


    def show(self):
        n = len(self.functions)
        self.fig, ax = plt.subplots(n, sharex=True)

        x = self.t
        for i, fun_dict in enumerate(self.functions):
            fun = fun_dict['fun']
            values = map(_param_init, fun_dict['params'])
            y = fun(x, *values)
            fun_dict['plot'], = ax[i].plot(x, y)
            x = y
            ax[i].axis([self.tmin, self.tmax, self.ymin, self.ymax])

        self._setup_sliders()
        plt.subplots_adjust(bottom=bottom + 2*height + slspace + margin)
        plt.show()

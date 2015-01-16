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


class Plot:

    def __init__(self, tfun, kfun, params, tmin=0, tmax=1, tstep=0.001, ymin=-10, ymax=10):
        self.tmin = tmin
        self.tmax = tmax
        self.ymin = ymin
        self.ymax = ymax
        self.t = np.arange(tmin, tmax, tstep)
        self.fun1 = tfun
        self.fun2 = kfun
        self.params = params
        self.sliders = []

    def _create_slider(self, param):
        i = len(self.sliders)
        axes = plt.axes([left, bottom + i*slspace, width, height])
        slider = Slider(axes, param['name'], param['min'], param['max'], valinit=_param_init(self.params[i]))
        self.sliders.append(slider)

    def _setup_sliders(self):
        for p in self.params:
            self._create_slider(p)

        def update(val):
            values = map(_slider_val, self.sliders)
            x = self.fun1(self.t, *values)
            X = self.fun2(x, *values)
            self.tplot.set_ydata(x)
            self.kplot.set_ydata(X)
            self.fig.canvas.draw_idle()

        for s in self.sliders:
            s.on_changed(update)

    def show(self):
        values = map(_param_init, self.params)
        x = self.fun1(self.t, *values)
        X = self.fun2(x, *values)

        self.fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        self.tplot, = ax1.plot(self.t, x)
        self.kplot, = ax2.plot(self.t, X)
        ax1.axis([self.tmin, self.tmax, self.ymin, self.ymax])
        ax2.axis([self.tmin, self.tmax, self.ymin, self.ymax])
        self._setup_sliders()

        plt.subplots_adjust(bottom=bottom + 2*height + slspace + margin)
        plt.show()

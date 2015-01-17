__author__ = 'victor'

from scipy.fftpack import fft
from scipy.signal import get_window

import numpy as np

from Plot import Plot



# util

def padded_window(wname, lenx, zpad):
    wlen = lenx*(1-zpad)
    w = get_window(wname, wlen)
    wpadded = np.zeros(lenx)
    start = lenx/2 - len(w)/2
    end = start + len(w)
    wpadded[start:end] = w
    return wpadded

# functions

def sin_wave(t, amp, freq):
    return amp * np.cos(2 * np.pi * freq * t)

def windowed_wave(x, zpad):
    w = padded_window('blackmanharris', len(x), zpad)
    return np.multiply(x, w)

def wave_fft(x):
    Xm = abs(fft(x))
    return np.log10(Xm)

# params
amp = dict(name='Amp', min=.1, max=10)
freq = dict(name='Freq', min=0, max=250)
zpad = dict(name='Z-Pad', min=0, max=1)

functions = [
    dict(fun=sin_wave, params=[amp, freq]),
    dict(fun=windowed_wave, params=[zpad]),
    dict(fun=wave_fft, params=[])
]

Plot(functions).show()

"""
Simulate propagation effects.
"""

import numpy as np


# This is the standard "rounded value" of
# the dispersion constant in use by pulsar
# astronomers (ref: pg. 129 of Manchester
# and Taylor 1977).
𝓓 = 1.0 / 2.41e-4


def disp(
    data: np.ndarray,
    dm: float,
    f0: float,
    df: float,
    dt: float,
) -> np.ndarray:

    """
    Disperse a frequency-time array.
    """

    nf, _ = data.shape
    f = np.linspace(start=f0, stop=(f0 + nf * df), num=nf)
    delays = (1.0 / f ** 2) - (1.0 / f0 ** 2)
    delays = dm * (𝓓 / dt) * (delays)
    delays = delays.astype(int)
    return np.asarray([np.roll(row, shift=delay) for row, delay in zip(data, delays)])


def codisp(
    data: np.ndarray,
    dm: float,
    f0: float,
) -> np.ndarray:

    """
    Disperse a voltage time series.
    """

    V = np.fft.rfft(data)
    f = np.fft.rfftfreq(data.size)
    H = 1j * 2 * np.pi * 𝓓 * (f ** 2) * dm
    H = H / (f + f0) * (f0 ** 2)
    H = np.exp(H)
    return np.fft.irfft(V * H)

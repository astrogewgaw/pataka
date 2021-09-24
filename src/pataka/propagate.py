"""
Simulate propagation effects.
"""

import numpy as np

from textwrap import dedent


# This is the standard "rounded value" of
# the dispersion constant in use by pulsar
# astronomers (ref: pg. 129 of Manchester
# and Taylor 1977).
𝓓 = 1.0 / 2.41e-4


def disperse(
    data: np.ndarray,
    dm: float,
    f0: float,
    df: float,
    dt: float,
) -> np.ndarray:

    """"""

    if data.ndim == 1:
        V = np.fft.rfft(data)
        f = np.fft.rfftfreq(data.size)
        H = 1j * 2 * np.pi * 𝓓 * (f ** 2) * dm
        H = H / (f + f0) * (f0 ** 2)
        H = np.exp(H)
        return np.fft.irfft(V * H)
    elif data.ndim == 2:
        nf, _ = data.shape
        f = np.linspace(start=f0, stop=(f0 + nf * df), num=nf)
        delays = (1.0 / f ** 2) - (1.0 / f0 ** 2)
        delays = dm * (𝓓 / dt) * (delays)
        delays = delays.astype(int)
        return np.vstack(
            [
                np.pad(
                    row,
                    pad_width=(pad, 0),
                )[:-pad]
                if pad != 0
                else row
                for row, pad in zip(data, delays)
            ]
        )
    else:
        raise ValueError(
            dedent(
                f"""
                The data has {data.ndim} dimensions, which is too many.
                This package can only generate one-dimensional voltage
                time series data or two-dimensional frequency-time data.
                Exiting...
                """
            )
            .replace("\n", " ")
            .strip()
        )

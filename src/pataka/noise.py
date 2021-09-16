"""
Generate power law noise.

This program is based on the algorithm proposed in "Om generating power law
noise", J. Timmer and M. König, Astron. Astrophys., 300, 707-710, 1995. The
generated noise has a spectrum S(ω) ∝ (1/ω) ** β, where β is known as the
spectral index. β is 1.0 for pink (or flicker) noise, and 2.0 for red noise.
Colored noise is encountered often in astronomical applications, especially
in radio astronomy, where the electronics itself introduces red noise into
the signal.
"""


import numpy as np


def noise(
    nt: int,
    nf: int = 1,
    beta: float = 2.0,
    cutoff: float = 0.0,
) -> np.ndarray:

    """
    Generate power law noise.

    Args:
        nt:     The number of samples in the time series.
        nf:     The number of frequency channels. If nf > 1, the noise being
                generated is a two-dimensional array, which is what we need for
                simulating frequency-time data. This is what is recorded by most
                radio telescopes for offline processing. For real-time processing,
                we wish to simulate voltage time series data, and we then set this
                value to 1.
        beta:   The spectral index of the noise. Since red noise is encountered more
                often in pulsar astronomy, this value is set to 2.0 by default.
        cutoff: The low frequency cutoff. The default value of 0.0 can be used to
                reproduce the analysis in the original paper. If cutoff < 1 / nt,
                its value is fixed to that limit, that is, cutoff =  1 / nt.
    """

    freqs = np.fft.rfftfreq(nt)

    scales = freqs.copy()
    cutoff = max(cutoff, 1.0 / nt)
    islice = np.sum(scales < cutoff)
    if islice and (islice < scales.size):
        scales[:islice] = scales[islice]
    scales = scales ** (-beta / 2.0)

    weights = scales[1:].copy()
    weights[-1] *= (1 + (nt % 2)) / 2.0
    stddev = 2 * np.sqrt(np.sum(weights ** 2.0)) / nt

    sizes = (nf, freqs.size)
    extras = 0 if nf == 1 else 1
    scales = scales[(np.newaxis,) * extras + (Ellipsis,)]

    srpow = np.random.normal(scale=scales, size=sizes)
    srphz = np.random.normal(scale=scales, size=sizes)

    if not (nt % 2):
        srphz[..., -1] = 0.0
    srphz[..., 0] = 0.0

    noise = (
        np.fft.irfft(
            srpow + 1j * srphz,
            n=nt,
            axis=-1,
        )
        / stddev
    )

    return noise[0] if nf == 1 else noise

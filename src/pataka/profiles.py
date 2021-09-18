"""
Generate pulse profiles.
"""

import numpy as np


def gaussian(
    nbins: int,
    width: float,
    offset: float,
    amplitude: float,
):

    """
    Generate a Gaussian pulse profile.

    The Gaussian distribution function is given by:

    f(x) = √(1 / 2πσ²) * exp(-(x-μ)²/2σ²),

    where μ is the mean and σ is the standard deviation of the probability
    distribution. The phase offset of the pulse is represented by the mean,
    and the width of the pulse can be represented in terms of the full width
    at half maximum (FWHM) of the peak, given in terms of σ as:

    FWHM = 2√(2ln2)σ.

    Args:
        nbins:      The number of bins in the profile.
        width:      The full width at half maximum (FWHM) of the pulse.
        offset:     The phase offset of the pulse from origin.
        amplitude:  The amplitude of the pulse.
    Returns:
        A array containing a Gaussian pulse profile.
    """

    x = np.arange(nbins, dtype=float)
    z = (x - (offset * nbins)) ** 2
    σ = width / (2 * np.sqrt(2 * np.log(2)))
    f = np.exp(-0.5 * (z / σ ** 2))
    f = f / np.sqrt(1 / (2 * np.pi * σ ** 2))
    f = f / f.max()
    f = amplitude * f
    return f


def vonmises(
    nbins: int,
    width: float,
    offset: float,
    amplitude: float,
):

    """
    Generate a von Mises profile.

    The von Mises distribution function is given by:

    f(x) = exp(κ * cos(x - μ)) / (2π * I₀(κ)),

    where κ is the von Mises factor, and I₀(κ) is a modified Bessel function
    of order zero. κ is a measure of concentration: the more the value of κ,
    the narrower the pulse is. We can therefore define the width of the pulse
    as 1/κ. The offset of the pulse is decided by the mean, μ, as it is for a
    Gaussian profile.

    Args:
        nbins:      The number of bins in the profile.
        width:      The width of the pulse.
        offset:     The phase offset of the pulse from origin.
        amplitude:  The amplitude of the pulse.
    Returns:
        A array containing a von Mises pulse profile.
    """

    δ = width / nbins
    κ = np.log(2.0) / (2.0 * np.sin(np.pi * δ / 2.0) ** 2.0)
    x = np.arange(nbins, dtype=float)
    z = (x / nbins - offset) * (2 * np.pi)
    f = np.exp(κ * (np.cos(z) - 1.0))
    f *= amplitude
    return f

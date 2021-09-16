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

    The Gaussian distribution function, for a given mean μ and standard deviation
    σ, can be written as: f(x) = (1/(σ * √2 * √π)) * exp(-0.5 * (x - μ)² / σ²).
    The width of the pulse can be defined as 1/σ². The offset of the pulse from
    origin is defined by the mean, μ. Since the above form is normalised, it can
    be scaled up to any desired amplitude by the multiplication of a simple scalar
    factor.

    Args:
        nbins:      The number of bins in the profile.
        width:      The width of the pulse.
        offset:     The phase offset of the pulse from origin.
        amplitude:  The amplitude of the pulse.
    Returns:
        A array containing a Gaussian pulse profile.
    """

    x = np.arange(nbins, dtype=float)
    z = (x - (offset * nbins)) ** 2
    f = np.exp(-0.5 * width * z)
    f *= amplitude * np.sqrt(width / (2 * np.pi))
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
    Gaussian profile. The above definition is normalised as well, and we can
    scale it up similarly by the desired amplitude.

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

import attr
import numpy as np
import matplotlib.pyplot as plt  # type: ignore

from textwrap import dedent

from .noise import noise
from .propagate import disp
from .propagate import codisp
from .profiles import vonmises
from .profiles import gaussian


@attr.s(repr=False, auto_attribs=True)
class Pulsar(object):

    """"""

    data: np.ndarray

    p: float
    dm: float
    nt: int
    nf: int
    dt: float
    df: float
    f0: float
    ducy: float
    snr: float
    offset: float
    spectral: float
    freqcut: float
    pulse: str

    @classmethod
    def make(
        cls,
        p: float,
        dm: float = 50.0,
        nt: int = 10000,
        nf: int = 1,
        dt: float = 512e-6,
        df: float = -(200.0 / 4096),
        f0: float = 500.0,
        ducy: float = 0.01,
        snr: float = 5.0,
        offset: float = 0.5,
        spectral: float = 2.0,
        freqcut: float = 0.0,
        pulse: str = "vonmises",
    ):

        """"""

        tobs = nt * dt
        nbins = np.ceil(p / dt)
        ncyc = np.ceil(tobs / p)

        ncyc = int(ncyc)
        nbins = int(nbins)
        width = ducy * nbins
        samples = ncyc * nbins

        N = noise(
            nt=nt,
            nf=nf,
            beta=spectral,
            cutoff=freqcut,
        )

        try:
            f = {
                "vonmises": vonmises,
                "gaussian": gaussian,
            }[pulse]
        except KeyError:
            raise NotImplementedError(
                dedent(
                    """
                    This type of pulse profile does not exist yet
                    in the pataka package. If you want to give it
                    a shot, send along a pull request via GitHub:
                    https://github.com/astrogewgaw/pataka.
                    """
                )
                .replace("\n", " ")
                .strip()
            )

        prof = f(
            nbins=nbins,
            width=width,
            offset=offset,
            amplitude=snr,
        )

        if nf == 1:
            data = np.concatenate([prof] * ncyc)[: (nt - samples)] + N
            data = codisp(data=data, dm=dm, f0=f0)
        elif nf > 1:
            data = (
                np.asarray([np.concatenate([prof] * ncyc)[: (nt - samples)]] * nf) + N
            )
            data = disp(
                data=data,
                dm=dm,
                f0=f0,
                df=df,
                dt=dt,
            )
        else:
            raise ValueError(
                dedent(
                    """
                    The number of frequency channels cannot be less than 1!
                    Exiting...
                    """
                )
                .replace("\n", " ")
                .strip()
            )

        return cls(
            data=data,
            p=p,
            dm=dm,
            nt=nt,
            nf=nf,
            dt=dt,
            df=df,
            f0=f0,
            ducy=ducy,
            snr=snr,
            offset=offset,
            spectral=spectral,
            freqcut=freqcut,
            pulse=pulse,
        )

    def plot(self):

        """"""

        if self.nf == 1:
            plt.plot(self.data)
            plt.xlabel("Time, $t$")
            plt.ylabel("Amplitude")
        else:
            plt.imshow(self.data)
            plt.xlabel("Time, $t$")
            plt.ylabel("Frequency, $\\nu$")

        plt.title(f"Pulsar simulated at P = {self.p} and DM = {self.dm}.")
        plt.show()

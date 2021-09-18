import attr
import numpy as np
import matplotlib.pyplot as plt  # type: ignore

from textwrap import dedent

from pataka.noise import noise
from pataka.propagate import disp
from pataka.propagate import codisp
from pataka.profiles import vonmises
from pataka.profiles import gaussian


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
    tobs: float
    ducy: float
    snr: float
    offset: float
    spectral: float
    pulse: str

    def __str__(self) -> str:
        return f"Pulsar (P = {self.p}, DM = {self.dm})"

    def __repr__(self) -> str:
        return str(self)

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
            cutoff=0.0,
            beta=spectral,
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
            data = np.concatenate([prof] * ncyc)[: (nt - samples)]
            data = codisp(data=data, dm=dm, f0=f0)
        elif nf > 1:
            data = np.asarray([np.concatenate([prof] * ncyc)[: (nt - samples)]] * nf)
            data = disp(data=data, dm=dm, f0=f0, df=df, dt=dt)
        else:
            raise ValueError(
                dedent(
                    """
                    The number of frequency channels cannot be less
                    than 1! Retry with a reasonable value for the 
                    number of channels. Exiting...
                    """
                )
                .replace("\n", " ")
                .strip()
            )

        data += N

        return cls(
            data=data,
            p=p,
            dm=dm,
            nt=nt,
            nf=nf,
            dt=dt,
            df=df,
            f0=f0,
            tobs=tobs,
            ducy=ducy,
            snr=snr,
            offset=offset,
            spectral=spectral,
            pulse=pulse,
        )

    def plot(self):

        """"""

        fig, ax = plt.subplots()

        if self.nf == 1:

            taxis = np.linspace(
                start=0.0,
                num=self.nt,
                stop=self.tobs,
            )

            ax.plot(taxis, self.data)
            ax.set_xlim([0, self.tobs])
            ax.set_xlabel("Time, $t$, in seconds.")
            ax.set_ylabel("Amplitude, in arbitrary units.")

        else:

            ax.imshow(self.data)
            ax.set_xlabel("Time, $t$, in seconds.")
            ax.set_ylabel("Frequency, $\\nu$, in MHz.")

        ax.set_title(str(self))
        fig.tight_layout()
        fig.show()

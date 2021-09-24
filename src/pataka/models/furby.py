import attr
import numpy as np
import matplotlib.pyplot as plt  # type: ignore

from textwrap import dedent

from pataka.noise import noise
from pataka.profiles import vonmises
from pataka.profiles import gaussian
from pataka.propagate import disperse


@attr.s(repr=False, auto_attribs=True)
class Furby(object):

    """"""

    data: np.ndarray

    dm: float
    nt: int
    nf: int
    dt: float
    df: float
    f0: float
    tobs: float
    width: float
    snr: float
    offset: float
    spectral: float
    pulse: str

    def __str__(self) -> str:
        return f"FRB (DM = {self.dm})"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def make(
        cls,
        dm: float = 500.0,
        nt: int = 10000,
        nf: int = 1,
        dt: float = 512e-6,
        df: float = -(200.0 / 4096),
        f0: float = 500.0,
        width: float = 0.01,
        snr: float = 5.0,
        offset: float = 0.5,
        spectral: float = 2.0,
        pulse: str = "vonmises",
    ):

        """"""

        tobs = nt * dt

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

        profile = f(
            nbins=nt,
            width=width,
            offset=offset,
            amplitude=snr,
        )

        if nf == 1:
            data = profile
        elif nf > 1:
            data = np.tile(profile, reps=(nf, 1))
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

        data = disperse(data=data, dm=dm, f0=f0, df=df, dt=dt)
        data = data + N

        return cls(
            data=data,
            dm=dm,
            nt=nt,
            nf=nf,
            dt=dt,
            df=df,
            f0=f0,
            tobs=tobs,
            width=width,
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

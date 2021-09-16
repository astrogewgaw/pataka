# type: ignore

from pathlib import Path
from setuptools import setup
from setuptools import find_packages


if __name__ == "__main__":
    setup(
        # Project metadata.
        name="pataka",
        author="Ujjwal Panda",
        author_email="ujjwalpanda97@gmail.com",
        description="Simulating cosmic fireworks 💻 💥 !",
        long_description=Path(__file__)
        .parent.resolve()
        .joinpath("README.md")
        .read_text(encoding="utf-8"),
        url="https://github.com/astrogewgaw/pataka",
        project_urls={
            "Documentation": "https://pataka.readthedocs.io",
            "Source": "https://github.com/astrogewgaw/pataka",
            "Issues": "https://github.com/astrogewgaw/pataka/issues",
            "Discussions": "https://github.com/astrogewgaw/pataka/discussions",
        },
        # PyPI keywords.
        keywords=[
            "FRBs",
            "pulsars",
            "modeling",
            "simulation",
            "radio astronomy",
        ],
        # PyPI classifiers.
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Topic :: Scientific/Engineering :: Astronomy",
        ],
        # Installation options.
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        setup_requires=["setuptools_scm[toml]>=6.0"],
        install_requires=[
            "numpy",
            "astropy",
            "matplotlib",
        ],
        install_package_data=True,
        zip_safe=False,
    )

# type: ignore

from invoke import task
from pathlib import Path

here = Path(__file__).parent.resolve()

name = "pataka"
src = here / "src"
docs = here / "docs"
tests = here / "tests"


@task
def clean(context):

    """
    Remove files used in testing and building this package, such as:

        * mypy's cache
        * pytest's cache
        * coverage reports
        * documentation build
        * nox virtual environments
        * tmp, dist, build and .eggs directories.
        * all .pyc files and __pycache__ directories.

    """

    context.run(f"rm -rf {here}/tmp")
    context.run(f"rm -rf {here}/dist")
    context.run(f"rm -rf {here}/build")
    context.run(f"rm -rf {here}/.nox")
    context.run(f"rm -rf {here}/.eggs")
    context.run(f"rm -rf {here}/.coverage")
    context.run(f"rm -rf {here}/.mypy_cache")
    context.run(f"rm -rf {here}/docs/build/*")
    context.run(f"rm -rf {here}/.pytest_cache")
    context.run("find . -type f -name '*.pyc' -delete")
    context.run("find . -type d -name '__pycache__' -delete")


@task
def install(context):

    """
    Install the package in development mode.
    """

    context.run(f"pip install -e {here}")


@task
def uninstall(context):

    """
    Uninstall the package.
    """

    context.run(f"pip uninstall {name}")
    context.run(f"rm -rf {src}/{name}.egg-info")


@task(clean)
def dist(context):

    """
    Build source distribution and wheel.
    """

    context.run("python setup.py sdist bdist_wheel")


@task
def upload_test(context):

    """
    Upload the distribution source to the TEST PyPI.

    This uploads the source distribution and the wheels to Test PyPI,
    which, as the name suggests, is meant for testing. That is, it is
    not the real packing index, but a clone where users upload their
    releases to see if everything is working properly, before uploading
    anything to the real PyPI.
    """

    context.run("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")


@task
def upload(context):

    """
    Upload the distribution source to the REAL PyPI.

    This uploads the source distribution and wheels to the real PyPI.
    Use only when you know what you are doing (that is, after you have
    tested everything out), because this is irreversible.
    """

    context.run("twine upload dist/*")


@task
def test(context):

    """
    Runs tests using nox.

    The nox package allows us to run tests on all supported Python
    versions, both locally and on the cloud (thanks to the GitHub
    Actions). It installs all dependencies in a virtual environment,
    and uses that for teesting, ensuring that we don't run into weird
    bugs that only arise on other people's systems and not my own.
    """

    context.run("nox -s test")


@task
def docs(context):

    """
    Serve documentation.

    This build the documentation for priwo (kept in the `docs`
    directory) and serves it locally, using `sphinx-autobuild`.
    This allows the user to see changes to the documentation as
    they edit it.
    """

    context.run(f"sphinx-autobuild {pkgdocs}/source {pkgdocs}/build")

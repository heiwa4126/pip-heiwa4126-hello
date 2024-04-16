import os
import sys

from invoke import task

os.environ["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
# ./src の下に置くのをやめれば、これは不要

PYTHON = "py" if sys.platform == "win32" else "python3"
PIP = "pip" if sys.platform == "win32" else "pip3"
VENVPIP = ".venv\\Scripts\\pip.exe" if sys.platform == "win32" else ".venv/bin/pip"

SCOPE = "heiwa4126"
PACKAGE = "hello"
PACKAGENAME = f"{SCOPE}.{PACKAGE}"


@task
def setup(c):
    """Setup virtual environment and install dependencies"""
    if not os.path.exists(".venv"):
        c.run(f"{PYTHON} -m venv .venv")
    c.run(f"{VENVPIP} install --use-pep517 -e .[dev] -U")
    # c.run(f"{VENVPIP} install -U -r requirements.txt")
    # c.run(f"{VENVPIP} install -U -r requirements-dev.txt")


@task
def example(c):
    """Run example code"""
    # c.run(f"{PYTHON} src/{SCOPE}/{PACKAGE}/hello.py")
    c.run(f"{PYTHON} examples/ex0.py")


@task
def cli(c):
    """Run cli.py code"""
    c.run(f"{PYTHON} -m {SCOPE}.{PACKAGE}.cli 15")


@task
def test(c):
    """Run unit tests"""
    if sys.platform == "win32":
        c.run(f"{PYTHON} -m unittest discover .\\tests -p test_*.py")
    else:
        c.run(f"{PYTHON} -m unittest discover ./tests -p 'test_*.py'")


@task
def build(c):
    """Build project"""
    if sys.platform == "win32":
        if os.path.exists("dist"):
            c.run("del /S /Q dist\\")
    else:
        c.run("rm -rf dist/*")
    c.run(f"{PYTHON} -m build")


@task
def install(c):
    """Install package locally"""
    os.environ["PYTHONPATH"] = ""
    c.run(f"{PIP} install -U dist/*.whl")


@task
def uninstall(c):
    """Uninstalls package locally"""
    os.environ["PYTHONPATH"] = ""
    c.run(f"{PIP} uninstall {PACKAGENAME} --yes")


@task
def reinstall(c):
    """uninstall, build and install"""
    uninstall(c)
    build(c)
    install(c)


@task
def check(c):
    """`ruff check .`"""
    c.run("ruff check .")


@task
def fix(c):
    """`ruff check . --fix`"""
    c.run("ruff check . --fix")


@task
def show(c):
    """`pip show package`"""
    c.run(f"{PIP} show {PACKAGENAME}")


@task
def listwhl(c):
    """`zipinfo dist/*.whl`"""
    c.run("zipinfo dist/*.whl")


@task
def listtarball(c):
    """`tar ztvf dist/*.tar.gz`"""
    c.run("tar ztvf dist/*.tar.gz")


@task
def release(c):
    """Release the project. same as `npm version patch` in Node.js."""
    import toml
    from packaging.version import Version, parse

    # Check if there are any uncommitted changes
    status = c.run("git status --porcelain", hide=True)
    if status.stdout:
        print("There are uncommitted changes. Please commit or stash them before releasing.")
        return

    # Read the current version from pyproject.toml
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)
        current_version = parse(config["project"]["version"])

    # Increment the patch version
    new_version = Version(f"{current_version.major}.{current_version.minor}.{current_version.micro + 1}")

    # Update the project version in pyproject.toml
    config["project"]["version"] = str(new_version)
    with open("pyproject.toml", "w") as f:
        toml.dump(config, f)

    # Commit the version change
    c.run(f"git commit -m 'Bump version to {new_version}' pyproject.toml")

    # Tag the commit with the new version
    c.run(f"git tag {new_version}")


@task
def push(c):
    """`git push & --tags`"""
    c.run("git push")
    c.run("git push --tags")


@task
def testpypi(c):
    """Upload to testpypi."""
    build(c)
    c.run(f"{PYTHON} -m twine upload --repository testpypi dist/*")


@task
def pypi(c):
    """Upload to pypi."""
    build(c)
    c.run(f"{PYTHON} -m twine upload --repository pypi dist/*")

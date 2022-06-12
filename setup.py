from setuptools import setup
from pathlib import Path 
import sys
import configparser

with open("README.md", "r") as fh:
    long_description = fh.read()

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))

config = configparser.ConfigParser()
config.read(CURRENT_DIR / "package.ini")

setup(
    name="dummyfilescreator",
    version=config["Info"]["version"],
    description=config["Info"]["description"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=config["Info"]["url"],
    author=config["Info"]["author"],
    author_email=config["Info"]["author_email"],
    license=config["Info"]["license"],
    packages=["dummyfilescreator"],
    include_package_data=True,
    install_requires=["PyQt5>=5.15.6", "tqdm>=4.64.0"],
    entry_points={
        "console_scripts": [
            "dummyfilescreator = dummyfilescreator.__main__:main"
        ]
    },
    python_requires='>=3.6', # f-strings
)

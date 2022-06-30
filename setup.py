import sys
import configparser
from pathlib import Path
from setuptools import setup

with open("doc/PyPi_description.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))

config = configparser.ConfigParser()
config.read(f"{CURRENT_DIR}/package.ini")

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
    install_requires=["PyQt5>=5.15.0", "tqdm>=4.64.0"],
    entry_points={
        "console_scripts": ["dummyfilescreator = dummyfilescreator.__main__:main"]
    },
    python_requires=">=3.6",  # f-strings
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Quality Assurance",
    ],
)

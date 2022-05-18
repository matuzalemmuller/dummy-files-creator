from setuptools import setup

setup(
    name="dummyfilescreator",
    version="3.0.0",
    description="Desktop & CLI tool to generate dummy files",
    url="https://github.com/matuzalemmuller/dummy-files-creator",
    author="Matuzalem (Mat) Muller",
    author_email="matuzalemtech@gmail.com",
    license="GPL v3",
    packages=["dummyfilescreator"],
    include_package_data=True,
    install_requires=["PyQt5>=5.15.6"],
    entry_points={
        "console_scripts": [
            "dummyfilescreator = dummyfilescreator.dummyfilescreator:main"
        ]
    },
)

from setuptools import setup

setup(
    name='Dummy Files Creator',
    version='3.0.0',    
    description='Desktop application to generate dummy files',
    url='https://github.com/matuzalemmuller/dummy-files-creator',
    author='Matuzalem (Mat) Muller',
    author_email='matuzalemtech@gmail.com',
    license='GPL-3.0',
    packages=['dummyfilescreator'],
    include_package_data=True,
    install_requires=['PyQt5==5.13.2'],
    entry_points = {
        "console_scripts": ['dummyfilescreator = dummyfilescreator.dummyfilescreator:main']
        },
)

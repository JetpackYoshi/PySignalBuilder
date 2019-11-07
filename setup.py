from setuptools import setup

setup(
    name='PySignalBuilder',
    version='0.1',
    packages=['SignalBuilder'],
    url='https://github.com/JetpackYoshi/PySignalBuilder',
    license='',
    author='Yoshin Govender',
    author_email='yoshin.govender@gmail.com',
    description='Python library for creating piecewise linear signals',
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ]
)

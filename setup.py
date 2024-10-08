from setuptools import find_packages, setup

__version__ = '0.0.4'

setup(
    name='lumberjack',
    version=__version__,
    description='The Lumberjack python logger.',
    keywords=['lumberjack', 'logger', 'package'],
    packages=find_packages(),
    install_requires=[
        'pydantic',
        'Requests',
        'colorama'
    ]
)

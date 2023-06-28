from setuptools import find_packages, setup

__version__ = '1.2.0'

setup(
    name='LumberjackLogger',
    version=__version__,
    description='The Lumberjack python logger.',
    keywords=['lumberjack', 'logger', 'package'],
    packages=find_packages(),
    install_requires=[
        'pydantic',
        'Requests'
    ]
)

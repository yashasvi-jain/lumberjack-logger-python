from setuptools import setup

__version__ = '1.1.0'

setup(
    name='LumberjackLogger',
    version=__version__,
    description='The Lumberjack python logger.',
    keywords=['lumberjack', 'logger', 'package'],
    packages=[
        'LumberjackLogger',
    ],
    install_requires=[
        'pydantic',
        'Requests'
    ]
)

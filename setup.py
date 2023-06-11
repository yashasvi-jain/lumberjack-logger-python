from setuptools import setup

setup(
    name='LumberjackLogger',
    version='1.0.0',
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
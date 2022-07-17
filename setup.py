from os.path import dirname, join

from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name='aiogram-inline-paginations',
    version=__version__,
    packages=find_packages(),
    url='',
    license='',
    author='Daniil Shamraev',
    author_email='shamraev.2002@gmail.com',
    description='',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiogram~=2.21'
    ]
)

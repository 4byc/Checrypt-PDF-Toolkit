from setuptools import setup, find_packages

setup(
    name='checrypt',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pikepdf',
        'tkinterdnd2'
    ],
    entry_points={
        'console_scripts': [
            'checrypt=checrypt.main:main'
        ]
    }
)

from setuptools import setup

setup(
    name="soragl",
    version="0.1",
    description="SoraGL - Game Engine",
    author="petthepotat",
    author_email="petrzhang20@gmail.com",
    packages=['soragl'],
    install_requires=[
        'pygame', 'moderngl', 'numpy'
    ],
)
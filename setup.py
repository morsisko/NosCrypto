import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="noscrypto",
    version="0.1.2",
    description="A reverse engineered packet cryptography - encryption and decryption routines to emulate NosTale client or server",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/morsisko/NosCrypto",
    author="morsisko",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    packages=["noscrypto", "noscrypto.tests"],
)

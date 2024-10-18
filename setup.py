from setuptools import find_packages, setup

setup(
    name="chainbase_python_sdk",
    version="0.0.1",
    description="A Python SDK for interacting with Chainbase APIs.",
    author="Panos",
    url="https://github.com/ppsimatikas/chainbase_python_sdk",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests==2.32.3",
        "pandas==2.1.3"
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

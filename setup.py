from setuptools import setup, find_packages

setup(
    name="chainbase_sdk",
    version="0.0.1",
    description="A Python SDK for interacting with Chainbase APIs.",
    author="Panos",
    url="https://github.com/ppsimatikas/chainbase_python_sdk",
    packages=find_packages(include=["src"], exclude=["tests"]),
    install_requires=[
        "requests==2.32.3",
        "pandas==2.1.3"
    ],
    license="MIT"
)

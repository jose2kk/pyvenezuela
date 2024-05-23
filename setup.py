from setuptools import setup, find_packages

setup(
    name="pyvenezuela",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    author="Jose Andres Morales",
    author_email="jose2kk@gmail.com",
    description="Python library that allows querying different Venezuela's data - such as BCV and CNE data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jose2kk/pyvenezuela",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
)

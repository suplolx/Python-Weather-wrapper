import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="darkskyapi-py",
    version="1.0.0",
    author="Hans Beijk",
    author_email="hans.beijk1992@gmail.com",
    description="A simple Python API wrapper for the DarkSky weather API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suplolx/Python-Weather-wrapper",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
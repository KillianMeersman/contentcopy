import setuptools
import const

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name=const.NAME,
    version=const.VERSION,
    author=const.AUTHOR,
    author_email=const.AUTHOR_EMAIL,
    description=const.DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=const.URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="contentcopy",
    version="1.0.0",
    author="Killian Meersman",
    author_email="hi@killianm.dev",
    description="Merge directory contents, deduplicating files based on their content.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KillianMeersman/contentcopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

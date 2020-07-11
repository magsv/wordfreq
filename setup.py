import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordfreq", 
    version="0.1",
    author="Magnus Svensson",
    author_email="magnus@massivemonster.org",
    license='Apache License 2.0',
    description="A small utiltity script to count frequencies of words in a text file including options to stem,remove uoms, remove numerics, remove decimals, lemmitization ",
    url = "https://github.com/magsv/wordfreq",
    packages=setuptools.find_packages(),
    install_requires=[
        'nltk>=3.5',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
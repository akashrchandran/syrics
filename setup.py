from setuptools import setup, find_packages

pkg_name = "syrics"


def read_file(fname):
    with open(fname, "r") as f:
        return f.read()


requirements = [
    "requests",
    "spotipy",
    "tqdm",
    "tinytag",
]

setup(
    name=pkg_name,
    version="0.0.1.7",
    author="Akash R Chandran",
    author_email="chandranrakash@gmail.com",
    description="A command line tool to fetch lyrics from spotify and save it to lrc file. It can fetch both synced and unsynced lyrics from spotify. ",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/akashrchandran/syrics",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "syrics = syrics:main",
        ],
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

# rm -f dist/*
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
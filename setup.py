import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dot-matrix-map",
    version="0.0.1",
    author="Alvin Lao",
    author_email="alvin.lao.is@gmail.com",
    description="Creates a dot matrix map image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alvinlao/dot-matrix-map",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

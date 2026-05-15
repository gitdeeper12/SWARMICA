"""Setup script for SWARMICA"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="swarmica-engine",
    version="1.0.0",
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="Variational and Continuum Mechanics Framework for Collective Stability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitedeeper12/SWARMICA",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0", "black>=22.0.0"],
    },
    entry_points={
        "console_scripts": [
            "swarmica=bin.swarmica_run:main",
        ],
    },
)

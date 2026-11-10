from setuptools import setup, find_packages
import os

long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="emochi-api",
    version="1.0.0",
    author="xellox",
    author_email="truong77kk@gmail.com",
    description="Python API Client for Emochi / FlowGPT AI Character Chat platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keksskks/emochi-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "websocket-client>=1.8.0",
        "deep-translator>=1.11.4"
    ]
)

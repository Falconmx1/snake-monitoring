#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="snake-monitoring",
    version="1.0.0",
    author="Falconmx1",
    author_email="tuemail@ejemplo.com",
    description="Monitor de sistema en tiempo real con interfaz retro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Falconmx1/snake-monitoring",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "snake-monitor=snake_monitor:main",
        ],
    },
)

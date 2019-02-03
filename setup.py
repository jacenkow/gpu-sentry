# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    "Flask>=1.0.2,<2",
    "nvidia-ml-py3>=7.352.0",
    "Twisted>=18.9.0",
    "requests>=2.20.1",
]

setup(
    name="gpu-sentry",
    author="Grzegorz Jacenków",
    author_email="grzegorz@jacenkow.com",
    install_requires=install_requires,
)

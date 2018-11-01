# coding: utf-8
import setuptools

setuptools.setup(
    name='cloudkeeper',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'websocket-client',
    ],
)

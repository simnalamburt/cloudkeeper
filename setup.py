# coding: utf-8
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cloudkeeper',
    version='1.0.0',
    author='Hyeon Kim',
    author_email='simnalamburt@gmail.com',
    description='Don\'t let IRCCloud disconnect you from the network.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/simnalamburt/cloudkeeper',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'websocket-client',
    ],
)

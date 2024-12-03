from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='advent_of_code_2024',
   version='1.0',
   description='A module for AdventOfCode solutions',
   license="MIT",
   long_description=long_description,
   author='Me',
   author_email='nomad@coronstreet.net',
   packages=['advent_of_code'],  #same as name
   install_requires=['wheel', 'bar'], #external packages as dependencies
)

from setuptools import find_packages, setup
setup(
    name='myanimelist',
    packages=find_packages(exclude='testes'),
    version='0.1.0',
    description='An easier way to work with both MyAnimeiList official API and Jikan API.',
    author='Ka_Knata',
    license='MIT',
    setup_requires=['requests']
)

'''
To setup the library:

1. Change the version
2. Delete trash files
3. Run in PowerShell
>>> python setup.py bdist_wheel
4. Reinstall the library by using 
>>> pip install C:\Users\victo\Documents\gitub\MAL-easy-client\dist\myanimelist-<VERSION>-py3-none-any.whl --force-reinstall
'''
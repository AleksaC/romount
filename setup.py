from setuptools import setup

from romount import __version__


with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='romount',
    version=__version__,
    author='Aleksa Ćuković',
    author_email='aleksacukovic1@gmail.com',
    description='CLI tool for mounting partitions in read-only mode.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/AleksaC/romount',
    license='MIT',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=requirements,
    packages=['romount'],
    entry_points={
        'console_scripts': ['romount = romount.romount:main']
    }
)

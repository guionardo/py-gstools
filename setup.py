"""Setup"""
import codecs
import os

from setuptools import find_packages, setup


def read(rel_path):
    """Read file content."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as file:
        return file.read()


def get_definitions(rel_path, *words):
    """Get definitions from package data file"""
    dwords = {word: None for word in words}
    for line in read(rel_path).splitlines():
        for word in words:
            if line.startswith(f'__{word}__'):
                delim = '"' if '"' in line else "'"
                dwords[word] = line.split(delim)[1]
                break

    return [dwords[word] for word in dwords]


long_description = read('README.md')

_name, _version, _description, _author, _author_email = get_definitions(
    os.path.join('gs', '__init__.py'),
    'tool_name',
    'version',
    'description',
    'author',
    'author_email')

DEV_STATUS = 'Development Status :: 4 - Beta'
try:
    version_numbers = [int(v) for v in _version.split('.')]
    if len(version_numbers) > 0:
        if version_numbers[0] > 0:
            DEV_STATUS = 'Development Status :: 5 - Production/Stable'
except Exception as exc:
    print('Error on getting version numbers', exc)


setup(
    name=_name,
    version=_version,
    description=_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        DEV_STATUS,
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    url='https://github.com/guionardo/py-gstools',
    keywords='tools',
    project_urls={
        "Documentation": "https://github.com/guionardo/py-gstools/wiki",
        "Source": "https://github.com/guionardo/py-gstools",
    },
    author=_author,
    author_email=_author_email,
    packages=find_packages(
        where=".",
        exclude=["tests"],
    ),
    install_requires=[
        'redis>=4.3.3',
        'PyYAML==6.0'
    ],
    zip_safe=True,
    python_requires='>=3.8.*'
)

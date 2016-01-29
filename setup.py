from os.path import abspath
from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup


def read_relative_file(filename):
    """
    Returns contents of the given file, whose path is supposed relative
    to this module.
    """
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()


setup(
    name='liberuditarticle',
    version=read_relative_file('VERSION').strip(),
    author='Erudit',
    author_email='info@erudit.org',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/erudit/liberuditarticle',
    license='GPLv3',
    description='A library to fetch Erudit data from fedora.',
    long_description=read_relative_file('README.md'),
    zip_safe=False,
    install_requires=[
        'eulxml',
        'eulfedora',
    ],
    dependency_links=[
        'git+ssh://git@github.com/erudit/eulxml.git@python3-support#egg=eulxml',
        'git+ssh://git@github.com/erudit/eulfedora.git@python3-support#egg=eulfedora',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

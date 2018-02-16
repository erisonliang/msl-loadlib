import sys
from distutils.cmd import Command
from setuptools import setup, find_packages

from msl import loadlib


class ApiDocs(Command):
    """
    A custom command that calls sphinx-apidoc
    see: http://www.sphinx-doc.org/en/latest/man/sphinx-apidoc.html
    """
    description = 'builds the api documentation using sphinx-apidoc'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from sphinx.apidoc import main
        main([
            'sphinx-apidoc',
            '--force',  # overwrite existing files
            '--module-first',  # put module documentation before submodule documentation
            '--separate',  # put documentation for each module on its own page
            '-o', './docs/_autosummary',  # where to save the output files
            'msl',
        ])
        sys.exit(0)


class BuildDocs(Command):
    """
    A custom command that calls sphinx-build
    see: http://www.sphinx-doc.org/en/latest/man/sphinx-build.html
    """
    description = 'builds the documentation using sphinx-build'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from sphinx import build_main
        build_main([
            'sphinx-build',
            '-b', 'html',  # the builder to use, e.g., create a HTML version of the documentation
            '-a',  # generate output for all files
            '-E',  # ignore cached files, forces to re-read all source files from disk
            'docs',  # the source directory where the documentation files are located
            './docs/_build/html',  # where to save the output files
        ])
        sys.exit(0)


def read(filename):
    with open(filename) as fp:
        text = fp.read()
    return text


# auto generate the MANIFEST.in file based on the platform
with open('MANIFEST.in', 'w') as f:
    f.write('# This file is automatically generated. Do not modify.\n')
    f.write('recursive-include msl/examples/loadlib *.cpp *.h *.cs *.f90\n')
    if 'sdist' not in sys.argv:
        f.write('recursive-include msl/loadlib {}*\n'.format(loadlib.SERVER_FILENAME))
        f.write('recursive-include msl/examples/loadlib *{}\n'.format(loadlib.DEFAULT_EXTENSION))
        if loadlib.IS_WINDOWS:
            f.write('include msl/loadlib/verpatch.exe\n')

testing = {'test', 'tests', 'pytest'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if testing else []

needs_sphinx = {'doc', 'docs', 'apidoc', 'apidocs', 'build_sphinx'}.intersection(sys.argv)
sphinx = ['sphinx', 'sphinx_rtd_theme'] if needs_sphinx else []

setup(
    name='msl-loadlib',
    version=loadlib.__version__,
    author=loadlib.__author__,
    author_email='joseph.borbely@measurement.govt.nz',
    url='https://github.com/MSLNZ/msl-loadlib',
    description='Load a shared library (and access a 32-bit library from 64-bit Python)',
    long_description=read('README.rst'),
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    setup_requires=sphinx + pytest_runner,
    tests_require=['pytest-cov', 'pytest', 'pathlib'],
    install_requires=['pythonnet>=2.3'] if not testing and loadlib.IS_WINDOWS else [],
    cmdclass={'docs': BuildDocs, 'apidocs': ApiDocs},
    packages=find_packages(include=('msl*',)),
    include_package_data=True,
)

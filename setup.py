from codecs import open
from os import path

from pkg_resources import parse_version
# Always prefer setuptools over distutils
# To use a consistent encoding
from setuptools import find_packages, setup

from boa3 import __version__ as version

here = path.abspath(path.dirname(__file__))

try:
    from pip._internal.req import parse_requirements
    from pip import __version__ as __pip_version
    pip_version = parse_version(__pip_version)
    if (pip_version >= parse_version("20")):
        from pip._internal.network.session import PipSession
    elif (pip_version >= parse_version("10")):
        from pip._internal.download import PipSession
except ImportError:  # pip version < 10.0
    from pip.req import parse_requirements
    from pip.download import PipSession

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the requirements from requirements.txt
install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = []
for ir in install_reqs:
    if hasattr(ir, 'requirement'):
        reqs.append(str(ir.requirement))
    else:
        reqs.append(str(ir.req))

setup(
    name='neo3-boa',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='A Python compiler for the Neo3 Virtual Machine',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    # The project's main homepage.
    url='https://github.com/CityOfZion/neo3-boa',

    # Author details

    # Choose your license
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    # What does your project relate to?

    keywords='compiler NEO .nef blockchain smartcontract development dApp',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().

    packages=find_packages(
        # do not include the compiler unit tests in the installed package
        exclude=('boa3_test.tests.*_tests*',),
        include=('boa3', 'boa3.*',
                 'boa3_test.tests', 'boa3_test.tests.*',
                 'test_runner', 'test_runner.*'),
    ),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=reqs,

    python_requires='>=3.7',

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['pycodestyle'],
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #    'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
       'console_scripts': [
           'neo3-boa=boa3.cli:main',
       ],
    },
)

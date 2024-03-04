from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='py-application-framework',
    version='1.0.0-alpha.1',
    author='David Runemalm, 2024',
    author_email='david.runemalm@gmail.com',
    description=
    'An application framework library for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/runemalm/py-application-framework',
    project_urls={
        "Documentation": "https://py-application-framework.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/runemalm/py-application-framework/issues",
    },
    package_dir={'': 'src'},
    packages = find_packages(
        where = 'src',
        include = ['application_framework*', ],
        exclude = ['tests*', ]
    ),
    entry_points={
        'console_scripts': [
            'application_framework = cli.main:main',
        ],
    },
    license='GNU General Public License v3.0',
    install_requires=[

    ],
    tests_require=[
        'pytest',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

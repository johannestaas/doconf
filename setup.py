import os
from setuptools import setup

# doconf
# Configuration specified through documentation, supporting multiple formats.


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="doconf",
    version="0.2.0",
    description=(
        "Configuration specified through documentation, supporting multiple "
        "formats."
    ),
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3",
    keywords="documentation configuration config conf cfg",
    url="https://github.com/johannestaas/doconf",
    packages=['doconf'],
    package_dir={'doconf': 'doconf'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'doconf=doconf:main',
        ],
    },
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    # package_data={
    #     'doconf': ['templates/*.html'],
    # },
    # include_package_data=True,
)

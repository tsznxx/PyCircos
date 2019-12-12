#! /usr/bin/env python
# coding: utf-8
# branch: dev
# version: 1.0.2
# license: AGPLv3
# author: Yunfei Wang (yfwang0405@gmail.com),
#         Baochen Yang (yangbaochen1217@gmail.com)


import os
import sys
from setuptools import setup, find_packages, Extension


def main():

    if float(sys.version[:3]) >= 3.5:
        # decsription
        with open("README.md", 'r') as md:
            long_description = md.read()
        setup(
            name='pycircos',
            version='1.0.2',
            author='Yunfei Wang, Baochen Yang',
            author_email='yfwang0405@gmail.com, yangbaochen1217@gmail.com',
            url='https://github.com/KimBioInfoStudio/PyCircos',
            license="AGPLv3",
            keywords="Python NGS Circos Plot",
            description=("This Tools is Design for NGS Circos Plot with using Python."),
            long_description=long_description,
            package_dir={'pycircos':'src'},
            packages=['pycircos'],
            scripts=[],
            ext_modules=[],
            classifiers=[
                'Environment :: Console',
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'License :: Free for non-commercial use',
                'License :: OSI Approved :: GNU General Public License (GPL)',
                # 'License :: OSI APPROVED :: GNU General Public License v3 (GPLv3)',
                'Operating System :: Unix',
                'Operating System :: POSIX :: Linux',
                'Operating System :: Microsoft :: Windows',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Topic :: Scientific/Engineering :: Bio-Informatics'
                           ],
            install_requires=['numpy','pandas','matplotlib'],
            python_requires='>=3.5')
    else:
        print("[ WARNING ]")
        print("As for www.python.org, Python2 will end life form 1/1/2020,")
        print("So we will not support Python form now on, and we deeply recommand")
        print("all our users to move to Python3.5+ ! Thx!")
if __name__ == '__main__':
    main()

#! /usr/bin/env python
# coding: utf-8 
# branch: dev
# version: 1.0.1
# license: BSD,AGPL
# author: Yunfei Wang (yfwang0405@gmail.com), 
#         Baochen Yang (yangbaochen1217@gmail.com)


import os,sys
from setuptools import setup, find_packages, Extension

def get_py_ver():
    return float(sys.version[:3])

if __name__ == '__main__':
    
    # decsription
    with open("README.rst",'r') as fh:
        long_description = fh.read()
        idx = long_description.find('\n')
        description = long_description[:idx].rstrip()
    
    # version
    PROG, VERSION = 'pycircos','1.0.1'

    # Compile Kent lib
    if 'clean' in sys.argv:
        print >> sys.stderr, "Clean dist and egg info ..."
        os.system('if [ -d dist ]; then rm -rf dist; fi')
        os.system('if [ -f {0}.egg-info ]; then rm {0}.egg-info; fi'.format(PROG))
        os.system('if [ -d {0}.egg-info ]; then rm -rf {0}.egg-info; fi'.format(PROG))
    
    # install requirement
    install_requires = [["numpy >= 1.4.1"],
                        ["pandas >= 0.18.0"]]
    # more options depends on python version
    if float(sys.version[:3]) <= 2.6:
        print("Sorry, We do recommand that you shoud  move to a new version fo python  than  Python3.5+ ")
        pass
    elif float(sys.version[:3]) == 2.7:
        print("Sorry, We do recommand that you shoud  move to a new version fo python  than  Python3.5+ ")
        package_dir={PROG:'v2'}
        install_requires.append(["matplotlib >= 2.0.2"])
    
    elif float(sys.version[:3]) >= 3.5:
        package_dir={PROG:'v3'}
        install_requires.append(["matplotlib >= 2.0.2"])

    setup(name=PROG,
          version=VERSION,
          author='Yunfei Wang, Baochen Yang',
          author_email='yfwang0405@gmail.com, yangbaochen1217@',
          url='https://github.com/tsznxx/{0}'.format(PROG),
          license="GNU General Public License (GPL)",
          keywords = "Python NGS plot",
          description = (description),
          long_description = long_description,
          package_dir=package_dir,
          packages = [PROG],
          scripts=[],
          ext_modules=[],
          classifiers=['Environment :: Console',
                       'Development Status :: 3 - Alpha',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: GNU General Public License (GPL)',
                       'License :: Free for non-commercial use',
                       'Operating System :: Unix',
                       'Programming Language :: Python :: 2.7',
                       'Topic :: Scientific/Engineering :: Bio-Informatics'],
          install_requires=install_requires)


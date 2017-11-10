#!/bin/sh
#Last-modified: 17 Jul 2017 11:02:25 AM

####################### Module/Scripts Description ######################
#  
#  Copyright (c) 2008 Yunfei Wang <tszn1984@gmail.com>
#  
#  This code is free software; you can redistribute it and/or modify it
#  under the terms of the BSD License (see the file COPYING included with
#  the distribution).
#  
#  @status:  experimental
#  @version: $Revision$
#  @author:  Yunfei Wang
#  @contact: tszn1984@gmail.com
#
#########################################################################


IFS='%'
USAGE=" Installation:\n    Usage 1: install to \$HOME/local\n        $0 install\n    Usage 2: install to a specified path\n        $0 path\n\n Uninstallation:\n    $0 uninstall\n\n Clean built files:\n    $0 clean\n\n Distribute:\n    $0 distribute\n"
case $# in
	0) echo -en $USAGE
	   exit;;
	*) ;;
esac

# Parse parameters
install_path=$1

# clean built files
if [ "$install_path" == "clean" ]; then
	python setup.py clean --all
elif [ "$install_path" == "distribute" ]; then
	python setup.py register sdist upload
# uninstall 
elif [ "$install_path" == "uninstall" ]; then
	if [ -f installed_files.txt ]; then
		cat installed_files.txt|xargs rm -rf
	fi
	rm installed_files.txt
# install
else
	if [ "$install_path" == "install" ]; then
		install_path=$HOME/TData/miniconda2
	fi
	# check if path exists
	if [ -d $install_path ]; then
		if [ -f installed_files.txt ]; then
			cat installed_files.txt|xargs rm -rf
		fi
		python setup.py install --record installed_files.txt --prefix=$install_path
	else
		echo "ERROR: Cannot parse the option, or the install path doesn't exist!"
	fi
fi


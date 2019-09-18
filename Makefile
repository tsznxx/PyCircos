.PHONY: hlep pre lint install test clean
.DEFAULT: help
help:
	@echo  "----------------------------------------"
	@echo  "PyCircos"
	@echo  "Design For NGS Circos Plot Within Python"
	@echo  "----------------------------------------"
	@echo  "make help"
	@echo  "\tprint this help info to screen"
	@echo  "make pre"
	@echo  "\tinstall needed env, use only once"
	@echo  "make lint"
	@echo  "\trun pylint to format all file"
	@echo  "make install"
	@echo  "\tinstall pycircos"
	@echo  "make test"
	@echo  "\trun a test demo"
	@echo  "make clean"
	@echo  "\tclean temp cache and unusing file"
pre:
	python3 -m pip install -r ./requirements.txt
lint:
	python3 -m pip install pylint
	python3 -m pylint
install:pre
	python3 ./setup.py install 
test:
	python3 ./test/test.py
clean:
	@rm -rf ./build ./dist ./pycircos.egg-info 




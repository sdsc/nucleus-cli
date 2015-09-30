all: clean requirements
	python setup.py install
	sphinx-apidoc -o docs/source cloudmesh_base
	cd docs; make -f Makefile html

view:
	open docs/build/html/index.html

requirements:
	pip install -r requirements-other.txt

######################################################################
# CLEANING
######################################################################

clean:
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;
	rm -rf build dist docs/build .eggs
	rm -rf *.egg-info
	# cd docs; make clean
	echo "clean done"

######################################################################
# TAGGING
######################################################################

tag:
	bin/new_version.sh

rmtag:
	git tag
	@echo "rm Tag?"; read TAG; git tag -d $$TAG; git push origin :refs/tags/$$TAG


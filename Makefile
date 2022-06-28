lint:
	pylint -j 4 --fail-under=9 $(git ls-files '*.py')
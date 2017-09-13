init:
	pip3 install -r requirements.txt

test:
	py.test tests/test.py --verbose --cov-report term --cov-report xml --cov imagesoup

flake8:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 imagesoup

publish:
	python3 setup.py sdist upload
	rm -fr build dist .egg imagesoup.egg-info

driver:
	python

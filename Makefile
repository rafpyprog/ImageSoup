init:
	python3.6 -m pip install -r requirements.txt -U

test:
	#py.test tests/test.py --verbose --cov-report term --cov-report xml --cov imagesoup
	#python3.5 -m pytest tests/test.py --verbose --cov-report term --cov-report xml --cov imagesoup
	python3.6 -m pytest tests/test.py --verbose --cov-report term --cov-report xml --cov imagesoup
	#python2.7 -m pytest tests/test.py --verbose --cov-report term --cov-report xml --cov imagesoup

flake8:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 imagesoup

publish:
	python3 setup.py sdist upload
	rm -fr build dist .egg imagesoup.egg-info

driver:
	python

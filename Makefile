lint:
	pylint -j4 ./aiojsonrpc


test:
	python3 -m unittest  tests/*_test.py
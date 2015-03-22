PYTHON = python3.4


test:
	$(PYTHON) -m unittest discover -v -p *Tests.py 




init:
	@echo "Creating virtual env and installing dependencies"
	python3 -m venv venv
	source venv/bin/activate && pip3 install -r requirements.txt

.PHONY: init
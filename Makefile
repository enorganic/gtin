install:
	python3 -m venv venv && \
	venv/bin/pip3 install -r requirements.txt -e .

clean:
	venv/bin/daves-dev-tools clean

gcp:
	venv/bin/python3 scripts/update_gcp_prefix_format_list.py

requirements:
	venv/bin/pip3 freeze --all --exclude gtin > requirements.txt

distribute:
	venv/bin/python3 scripts/update_gcp_prefix_format_list.py
	daves-dev-tools distribute --skip-existing

test:
	venv/bin/tox -e py

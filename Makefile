install:
	python3 -m venv venv && \
	venv/bin/pip3 install -r requirements.txt -e .

clean:
	venv/bin/daves-dev-tools clean

update-gcp-prefix-format-list:
	venv/bin/python3 scripts/update_gcp_prefix_format_list.py

requirements:
	venv/bin/pip3 freeze --all --exclude gtin > requirements.txt

distribute:
	update-gcp-prefix-format-list
	daves-dev-tools distribute --skip-existing

test:
	venv/bin/tox -e py

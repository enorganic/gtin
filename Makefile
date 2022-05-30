# python 3.6 is used, for the time being, in order to ensure compatibility
install:
	{ python3.6 -m venv venv || python3 -m venv venv || \
	py -3.6 -m venv venv || py -3 -m venv venv ; } && \
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && \
	python3 -m pip install --upgrade pip && \
	python3 -m pip install\
	 -r requirements.txt\
	 -e . --ignore-requires-python && \
	mypy --install-types --non-interactive ;

editable:
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && \
	daves-dev-tools install-editable --upgrade-strategy eager && \
	make upgrade

clean:
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && \
	daves-dev-tools uninstall-all\
	 -e .\
     -e pyproject.toml\
     -e tox.ini\
     -e requirements.txt && \
	daves-dev-tools clean

distribute:
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && \
	python3 scripts/update_gcp_prefix_format_list.py && \
	daves-dev-tools distribute --skip-existing

upgrade: 
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && \
	daves-dev-tools requirements freeze\
	 -nv '*' . pyproject.toml tox.ini daves-dev-tools \
	 > .unversioned_requirements.txt && \
	python3 -m pip install --upgrade --upgrade-strategy eager\
	 -r .unversioned_requirements.txt && \
	rm .unversioned_requirements.txt && \
	make requirements

requirements:
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && \
	daves-dev-tools requirements update\
	 -aen all\
	 setup.cfg pyproject.toml tox.ini && \
	daves-dev-tools requirements freeze\
	 -nv setuptools -nv filelock -nv platformdirs\
	 . pyproject.toml tox.ini daves-dev-tools\
	 > requirements.txt

test:
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && tox -r -p

gcp:
	{ . venv/bin/activate || venv/Scripts/activate.bat ; } && \
	venv/bin/python3 scripts/update_gcp_prefix_format_list.py]

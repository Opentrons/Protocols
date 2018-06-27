SHELL := /bin/bash

MONOREPO_URI := https://github.com/Opentrons/opentrons.git
OT1_VERSION := 2.5.2
OT2_VERSION_TAG := v3.2.0-beta.1
OT2_MONOREPO_DIR := ot2monorepoClone

OT1_FILE_SUFFIX := *.ot1.py
OT2_FILE_SUFFIX := *.ot2.py

.PHONY: install
install:
	pip install virtualenv

venvs:
	mkdir venvs/

venvs/ot1: venvs
	virtualenv venvs/ot1 && \
	source venvs/ot1/bin/activate && \
	pip install opentrons==$(OT1_VERSION) && \
	deactivate

.PHONY: parse-ot1
parse-ot1: venvs/ot1
	source venvs/ot1/bin/activate && \
	find protocols/ -name $(OT1_FILE_SUFFIX) | xargs python protolib2/parseOT1.py && \
	deactivate

ot2monorepoClone:
	git clone --depth=1 --branch=$(OT2_VERSION_TAG) $(MONOREPO_URI) $(OT2_MONOREPO_DIR)

venvs/ot2: ot2monorepoClone
	virtualenv venvs/ot2 && \
	source venvs/ot2/bin/activate && \
	pip install -r $(OT2_MONOREPO_DIR)/api/requirements.txt && \
	pushd $(OT2_MONOREPO_DIR)/api/ && \
	python setup.py install && \
	popd && \
	deactivate

# OVERRIDE_SETTINGS_DIR must be set to use opentrons v3
# (otherwise it will try to access /data dir during 'import opentrons')
.PHONY: parse-ot2
parse-ot2: venvs/ot2
	source venvs/ot2/bin/activate && \
	export OVERRIDE_SETTINGS_DIR=$(OT2_MONOREPO_DIR)/api/tests/opentrons/data && \
	find protocols/ -name $(OT2_FILE_SUFFIX) | xargs python protolib2/parseOT2.py && \
	deactivate

.PHONY: clean
clean:
	rm -rf $(OT2_MONOREPO_DIR) venvs

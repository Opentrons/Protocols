SHELL := /bin/bash

PROTOCOLS_PYTHON ?= python

MONOREPO_URI := https://github.com/Opentrons/opentrons.git
OT2_VERSION_TAG := v6.1.0
OT2_MONOREPO_DIR := ot2monorepoClone

# Parsers output to here
BUILD_DIR := protoBuilds

# Ignore all protocol dirs that contain a file named '.ignore'
# on the top protocol folder level
IGNORED_INPUT_PATHS := $(addsuffix %, $(dir $(wildcard protocols/*/.ignore)))

OT2_INPUT_FILES_UNFILTERED := $(shell find protocols -type f -name '*.ot2.apiv2.py')
OT2_INPUT_FILES := $(filter-out $(IGNORED_INPUT_PATHS), $(OT2_INPUT_FILES_UNFILTERED))
OT2_OUTPUT_FILES := $(patsubst protocols/%.ot2.apiv2.py, $(BUILD_DIR)/%.ot2.apiv2.py.json, $(OT2_INPUT_FILES))

pip_install := ${PROTOCOLS_PYTHON} -m pip install


.PHONY: all
all: parse-ot2 parse-errors parse-README
	$(MAKE) build

.PHONY: clone-repo
clone-repo:
	git clone --depth=1 --branch=$(OT2_VERSION_TAG) $(MONOREPO_URI) $(OT2_MONOREPO_DIR)

.PHONY: setup
setup: clone-repo
	${pip_install} virtualenv flake8==3.7.9 pytest
	$(MAKE) venvs/ot2

venvs/ot2:
	pip install -e otcustomizers && \
	pip install -r protolib/requirements.txt && \
	pushd $(OT2_MONOREPO_DIR)/api/ && \
	$(MAKE) setup && \
	python setup.py install && \
	popd && \
	deactivate

.PHONY: parse-errors
parse-errors:
	python protolib/traverse_errors.py

.PHONY: parse-ot2
parse-ot2: $(OT2_OUTPUT_FILES)

# Parse all OT2 python files
# Note: OVERRIDE_SETTINGS_DIR must be set to use opentrons v3
$(BUILD_DIR)/%.ot2.apiv2.py.json: protocols/%.ot2.apiv2.py
	mkdir -p $(dir $@)
	source venvs/ot2/bin/activate && \
	export OVERRIDE_SETTINGS_DIR=$(OT2_MONOREPO_DIR)/api/tests/opentrons/data && \
	python protolib/parse/parseOT2v2.py $< $@ && \
	python protolib/parse/parseREADME.py $< $@ && \
	python scripts/pd-generate.py $< && \
	python scripts/fields_mine.py $< && \
	deactivate

.PHONY: parse-README
parse-README:
	source venvs/ot2/bin/activate && \
	python protolib/traverse_README.py && \
	deactivate

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)

.PHONY: teardown
teardown:
	rm -rf $(OT2_MONOREPO_DIR) venvs

# Take all files in BUILD_DIR and make a single zipped JSON
.PHONY: build
build:
	python -m protolib

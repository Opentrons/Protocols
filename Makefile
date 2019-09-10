SHELL := /bin/bash

MONOREPO_URI := https://github.com/Opentrons/opentrons.git
OT1_VERSION := 2.5.2
OT2_VERSION_TAG := v3.11.4
OT2_MONOREPO_DIR := ot2monorepoClone
OT1_TEMP_DIR := ot1temp
# Parsers output to here
BUILD_DIR := protoBuilds

# Ignore all protocol dirs that contain a file named '.ignore'
# on the top protocol folder level
IGNORED_INPUT_PATHS := $(addsuffix %, $(dir $(wildcard protocols/*/.ignore)))

OT1_INPUT_FILES_UNFILTERED := $(shell find protocols -type f -name '*.ot1.py')
OT1_INPUT_FILES := $(filter-out $(IGNORED_INPUT_PATHS), $(OT1_INPUT_FILES_UNFILTERED))
OT1_OUTPUT_FILES := $(patsubst protocols/%.ot1.py, $(BUILD_DIR)/%.ot1.py.json, $(OT1_INPUT_FILES))

OT2_INPUT_FILES_UNFILTERED := $(shell find protocols -type f -name '*.ot2.py')
OT2_INPUT_FILES := $(filter-out $(IGNORED_INPUT_PATHS), $(OT2_INPUT_FILES_UNFILTERED))
OT2_OUTPUT_FILES := $(patsubst protocols/%.ot2.py, $(BUILD_DIR)/%.ot2.py.json, $(OT2_INPUT_FILES))

.PHONY: all
all: parse-ot1 parse-ot2 parse-errors parse-README
	$(MAKE) build

ot2monorepoClone:
	git clone --depth=1 --branch=$(OT2_VERSION_TAG) $(MONOREPO_URI) $(OT2_MONOREPO_DIR)

.PHONY: setup
setup:
	$(MAKE) ot2monorepoClone
	python -m pip install virtualenv
	$(MAKE) venvs/ot1 venvs/ot2

venvs/ot1:
	mkdir -p venvs
	virtualenv venvs/ot1
	source venvs/ot1/bin/activate && \
	pip install opentrons==$(OT1_VERSION) && \
	pip install -e otcustomizers && \
	pip install -r protolib2/requirements.txt && \
	deactivate

venvs/ot2:
	mkdir -p venvs
	virtualenv venvs/ot2
	source venvs/ot2/bin/activate && \
	pip install -e otcustomizers && \
	pip install -r protolib2/requirements.txt && \
	pip install pipenv && \
	pushd $(OT2_MONOREPO_DIR)/api/ && \
	$(MAKE) install && \
	python setup.py install && \
	popd && \
	deactivate

.PHONY: parse-errors
parse-errors:
	python protolib2/traverse_errors.py

# TODO: Ian 2019-03-11 maybe ot1 can be parallelized somehow.
# right now it deletes `configurations.json` and runs into race conditions
# deleting that file after another process just deleted it
.PHONY: parse-ot1
parse-ot1: $(OT1_OUTPUT_FILES)

# Parse all OT1 python files
$(BUILD_DIR)/%.ot1.py.json: protocols/%.ot1.py
	mkdir -p $(dir $@)
	source venvs/ot1/bin/activate && \
	APP_DATA_DIR=$(OT1_TEMP_DIR)/$@ python protolib2/parse/parseOT1.py $< $@ && \
	deactivate

.PHONY: parse-ot2
parse-ot2: $(OT2_OUTPUT_FILES)

# Parse all OT2 python files
# Note: OVERRIDE_SETTINGS_DIR must be set to use opentrons v3
$(BUILD_DIR)/%.ot2.py.json: protocols/%.ot2.py
	mkdir -p $(dir $@)
	source venvs/ot2/bin/activate && \
	export OVERRIDE_SETTINGS_DIR=$(OT2_MONOREPO_DIR)/api/tests/opentrons/data && \
	python protolib2/parse/parseOT2.py $< $@ && \
	deactivate

.PHONY: parse-README
parse-README:
	source venvs/ot2/bin/activate && \
	python protolib2/traverse_README.py && \
	deactivate

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)

.PHONY: teardown
teardown:
	rm -rf $(OT2_MONOREPO_DIR) venvs $(OT1_TEMP_DIR)

# Take all files in BUILD_DIR and make a single zipped JSON
.PHONY: build
build:
	python -m protolib2

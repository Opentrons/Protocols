#!/usr/bin/env bash
pip install virtualenv

OT2_VERSION_TAG=v3.2.0-beta.1
MONOREPO_URI=https://github.com/Opentrons/opentrons.git
OT2_MONOREPO_DIR=ot2monorepoClone

# OT1 env var setup & parsing
virtualenv ot1env
source ot1env/bin/activate
# install OT2 opentrons from PyPI
pip install opentrons
find protocols/ -name *.ot1.py | xargs python protolib2/parseOT1.py
deactivate

# OT2 env var setup & parsing
virtualenv ot2env
source ot2env/bin/activate
git clone --depth=1 --branch=$OT2_VERSION_TAG $MONOREPO_URI $OT2_MONOREPO_DIR
echo '----- INSTALLING OPENTRONS API FOR OT2 -----'
make -C $OT2_MONOREPO_DIR/api install
echo '----- PARSING OT2 PROTOCOLS -----'
find protocols/ -name *.ot2.py | xargs python protolib2/parseOT2.py
deactivate

# TODO: parse READMEs

# cleanup TODO
rm -rf $OT2_MONOREPO_DIR ot1env ot2env

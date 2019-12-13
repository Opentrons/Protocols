#!/bin/bash

# exit with error status if `make parse-ot2` has work to do
if ! make parse-ot2 --question; then
    echo '***** MISSING UPDATES TO PROTOBUILDS (.py protocol files): *****';
    make parse-ot2 --dry-run;
    exit 1;
fi

# exit with error status if errors/readmes have uncommited updates
make parse-errors parse-README > /dev/null;
if [[ $(git ls-files --modified protoBuilds) ]]; then
    echo '***** MISSING UPDATES TO PROTOBUILDS (metadata/readme files): *****';
    git ls-files --modified protoBuilds;
    exit 1;
fi

echo 'protoBuilds appears up-to-date!'
#!/bin/bash

# exit with error status if `make parse-ot2` has work to do
# NOTE: this doesn't work b/c make uses timestamps and git does not preserve them.
# if ! make parse-ot2 --question; then
#     echo '***** MISSING UPDATES TO PROTOBUILDS (.py protocol files): *****';
#     make parse-ot2 --dry-run;
#     exit 1;
# fi

# exit with error status if errors/readmes have uncommited updates
echo 'parsing errors & readmes...'
make parse-errors parse-README;
if [[ $(git ls-files --modified protoBuilds) ]]; then
    echo '***** MISSING UPDATES TO PROTOBUILDS (metadata/readme files): *****';
    git ls-files --modified protoBuilds;
    exit 0;
fi

echo 'protoBuilds appears up-to-date!'

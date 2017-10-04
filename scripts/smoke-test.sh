#!/usr/bin/env bash

# Clean smoketest dir
rm -rf smoketest/*.py

echo "Ignoring:"
find . -name '*.ignore.py'

echo "*****"

# copy all non-ignored .py files to smoketest/
find . -name '*.py' | grep -Ev '.*\.ignore\.py|.*/scripts/' | sort -f | while read filename; do
    cp $filename smoketest/
done

find smoketest/ -name '*.py' | sort -f | while read pyfile; do
  if grep -Eq "^def run_protocol\(" $pyfile; then
    echo "Processing CUSTOMIZABLE protocol '$pyfile'"
    # add run_protocol() call to end of all customizable protocols
    echo 'run_protocol()' >> $pyfile
  else
    echo "Processing protocol '$pyfile'"
  fi

  python "$pyfile" || exit 1
done

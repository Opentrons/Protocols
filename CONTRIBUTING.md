# Installation / Setup

Run this in your terminal. Pip is required.

WARNING: this will install flake8, pytest, and virtualenv in your current global python environment.

```bash
pip install -e otcustomizers
pip install -r protolib/requirements.txt
pip install flake8==3.5.0 pytest
make install
```

# Generating derived data

To speed up CI, we commit the results of these parsers to git. To run all the parsers, do:

`make parse-errors parse-ot1 parse-ot2 parse-README`

Run this yourself locally before each PR!

Then, **commit** the changed files in `protoBuilds/`.

To run the parsers quicker, add a `-j` argument to run jobs in parallel:
eg `make parse-ot2 -j`. WARNING: this often fails for `make parse-ot1` because
the old OT1 python API does not handle multiple instances well - eg it frequently
deletes `configurations.json` and there can be race conditions where processes
fail because they attempt to delete it and it's already just been deleted.

Parsers will **skip** parsing a file when the output JSON file exists and has a more recent timestamp than the source file (eg the output file `protoBuild/exampleProtocol/example.ot2.py.json` corresponds to the source file `protocols/exampleProtocol/example.ot2.py`). To make sure that the parsers do not skip anything, delete the output file and run the parser again.

If you have problems with the code not matching the website, try doing `make clean install` and then run the parsers again.

# Installation / Setup

Run this in your terminal. Pip is required.

WARNING: this will install flake8, pytest, and virtualenv in your current global python environment.

```bash
pip install -e otcustomizers
pip install -r protolib/requirements.txt
pip install flake8==3.5.0 pytest
make setup
```

# Generating derived data

To speed up CI, we commit the results of these parsers to git. To run all the parsers in parallel, do:

`make all -j`

Run this yourself locally before each PR!

Then, **commit** the changed files in `protoBuilds/`.

OT1 and OT2 parsers will **skip** parsing a file when the output JSON file exists and has a more recent timestamp than the source file (eg the output file `protoBuild/exampleProtocol/example.ot2.py.json` corresponds to the source file `protocols/exampleProtocol/example.ot2.py`). If you want to re-parse a file, delete the output file and run the parser again.

If you have problems with the code not matching the website, try doing `make teardown clean setup` to get a fresh setup, then run the parsers again with `make all -j`.

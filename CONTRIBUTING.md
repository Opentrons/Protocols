# Installation / Setup

```bash
pip install -e otcustomizers
pip install -r protolib/requirements.txt
pip install flake8==3.5.0 pytest
make install
```

# Generating derived data

Run this yourself locally before each PR! To speed up CI, we commit the results of these parsers

`make parse-errors parse-ot1 parse-ot2 parse-README`

Commit the changed files in `protoBuilds/`

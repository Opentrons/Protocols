# `protolib` - Protocol Library protocol parser

Protolib traverses through a directory of protocols, parses supported files inside each protocol subdirectory, and creates a JSON intended for use by Opentrons Protocol Library: http://protocols.opentrons.com

## Supported protocol files

Inside `protocols/`, each subdirectory represents a single protocol and can contain these files:

* `*.ot1.py`: OT1 Python protocol file
* `*.ot2.py`: OT2 Python protocol file
* `*.md` (preferably `README.md`): README files for a protocol following a specific Markdown format

### README format

See `TEMPLATE/README.md` for a (SOMEWHAT OUTDATED) example of the README format.

Note that the `subcategory` section must be indented by a tab, not by spaces.

## Use in development

From the repo root:

```bash
# inside a virtualenv
pip install -r protolib/requirements.txt

# build zipped JSON of protocols & categories from
# all protocols in the protocols/ directory
# and put the result in the releases/ dir
python -m protolib protocols/ releases/
```


## Output JSON format

Contains 2 keys: `protocols` & `categories`

### `categories`

An object of the form:

```json
"categories": {
  "Proteins & Proteomics": [
    "Assay",
    "ELISA",
    "Protein Crystallography",
    "Sample Prep"
  ],
  "Cell Culture": [
    "Media Exchange"
  ]
}
```

### `protocols`

An arbitrarily-ordered array of protocol objects.

A single protocol object is of the form:

```json
{
  "slug": "exampleProtocol",
  "path": "protocols/exampleProtocol",
  "flags": {
    "ignore": false,
    "feature": false,
    "skip-tests": false,
    "embedded-app": false
  },
  "detected-files": {
    "description": [
      "README.md"
    ],
    "OT 1 protocol": [
      "exampleProtocol.ot1.py"
    ],
    "OT 2 protocol": [
      "exampleProtocol.ot2.py"
    ]
  },
  "status": "ok",
  "errors": [],
  "files": {
    "description": "README.md",
    "OT 1 protocol": "exampleProtocol.ot1.py",
    "OT 2 protocol": "exampleProtocol.ot2.py"
  },
  "instruments": [
    {
      "name": "p50multi",
      "axis": "a",
      "channels": 8,
      "type": "pipette",
      "min_volume": 5,
      "max_volume": 50
    }
  ],
  "containers": [
    {
      "type": "tiprack-200ul",
      "slot": "A1",
      "name": "cool tiprack"
    }
  ],
  "parameters": [
    {
      "name": "plate_number",
      "annotation": {
        "type": "int"
      },
      "default": 4
    }
  ],
  "title": "Example Protocol",
  "author": "Opentrons",
  "partner": "",
  "categories": {
    "Demos": [
      "Examples"
    ]
  },
  "description": "An example protocol.",
  "time-estimate": "2 minutes",
  "robot": [
    "OT PRO",
    "OT Standard",
    "OT Hood"
  ],
  "modules": [],
  "reagents": [
    "Buffer",
    "DNA"
  ],
  "process": "Process details here",
  "notes": "Notes here",
  "internal": "Internal code for record-keeping",
  "markdown": /* auto-generated parsed markdown JSON goes here */
},
```

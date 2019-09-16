# Opentrons Protocol Library

This is where Opentrons protocols are stored for everyone to use.

The `master` branch populates http://protocols.opentrons.com/, our Protocol Library. Please let us know if you would like to contribute your protocols, or just submit a pull request. We would love to add your Opentrons protocols to the Library!

All the best,

Will Canine
Co-Founder, Opentrons
will@opentrons.com

# Contributing

## `develop` staging branch

The `develop` branch populates the staging version of the Opentrons Protocol Library at http://develop.protocols.opentrons.com/. Pull requests should be made to `develop` to be staged, and we will merge the changes into `master` as a second step.

# Formatting protocols

Every protocol needs its own folder. In that folder, there needs to be:

- A single `README.md` readme file
- A single `.py` [Opentrons protocol](http://docs.opentrons.com) file
- Optional "dot files" (see below)

## README file format

Every protocol should have a README file in its folder, with the file name `README.md`. It is a [Markdown](https://daringfireball.net/projects/markdown/syntax) file, with a specific format. See `template/README.md` for an example.

## "Dot files"

"Dot files" are files inside a protocol folder which start with a dot (`.`).

These files are usually blank text files. They have special names that indicate specific properties for that protocol:

- `.feature` - The protocol will be listed under "Featured Protocols" on the website.
- `.ignore` - The protocol will not be shown on the Opentrons Protocol Library, even if you search for it.
- `.notests` - The protocol will not be tested by continuous integration. This is intended only for ignored protocols.
- `.embedded` - This is for "embedded apps" that generate a protocol and are designed to be shown in the Protocol Library in an iframe. This file should not be blank, it should contain a URL to the web app that will be embedded in the iframe.
- `.hide-from-search` - do not show this protocol in any search results. The protocol page should only be accessible from direct URL.

# Writing Custom Protocols

## NOTE

Custom protocols is an early-stage feature, under active development. They are subject to change.

## Part 1: Set up basic protocol

In the Protocol APIv2 `def run(context):` function, use `context` to load your pipettes, labware, and modules. Proceed with the protocol steps.

For some protocols, you might want "number of destination plates" to be a variable. However, the deck map on the website is currently not dynamic - it will only show containers loaded at the top of the file. For this reason, you should load all the containers you might need in the first lines of the `run` function body, and then only use what you need during the actual execution.

**PLEASE NOTE!** The convention for APIv2 protocol file names is `protocols/{NAME}/{NAME}.ot2.apiv2.py`. The "{NAME}" should match the name of the folder in protocols. Eg in the folder `protocols/my_cool_protocol/` the Python file should be called `my_cool_protocol.ot2.apiv2.py`.

## Part 2: Set your customizable arguments

To make a protocol customizable, write a `fields.json` file and save it in the protocol folder, as a sibling of the `.ot2.apiv2.py` file. Eg `protocols/my_cool_protocol/fields.json`.

The information in the `fields.json` file will be used to create input forms on the Protocol Library website page for your protocol, which get passed into the protocol.

The `fields.json` file should be an array of field objects. Here's an example:

```json
[
  {
    "type": "float",
    "label": "Master Mix Volume (uL)",
    "name": "master_mix_volume",
    "default": 20
  },
  {
    "type": "int",
    "label": "Integer example",
    "name": "integer_example",
    "default": 10
  },
  {
    "type": "dropDown",
    "label": "Example Dropdown",
    "name": "example_dropdown",
    "options": [
      { "label": "Something here", "value": "aaa" },
      { "label": "Other thing", "value": "bbb" }
    ]
  },
  {
    "type": "textFile",
    "label": "Example file",
    "name": "example_file",
    "default": "1,2,3"
  }
]
```

### Get values in the Python protocol with `get_values`

To allow you to get the parametric values inside the protocol, a function `def get_values(*names)` will be injected into the Python protocol when a user downloads the protocol from the site.

```py
import opentrons

def run(context):
    example_dropdown, integer_example, float_example, example_file = get_values(  # noqa: F821
        'example_dropdown', 'integer_example', 'float_example', 'example_file')

    # ... do stuff with those values
```

#### Linting error?

You should expect to get a linting error: `[F821] undefined name 'get_values'`. That's OK, because the special `get_values` fn will be injected into the
protocol at download time.

To avoid this linting error from failing the build in CI, make sure to add `# noqa: F821` inline with all calls to `get_values`

### `name`

This field is used as an ID for accessing a field. If you have a field with `"name": example_field"` in `fields.json`, in the Python protocol you use that same name to get the value `get_values('example_field')`

Each field must have a unique `name`, otherwise unexpected behavior may occur.

### `type`

The `type` field specifies what kind of input field you want. The options are `float`, `int`, `dropDown`, or `textFile`.

### `label`

This is the human-readable label shown on the website describing what the user should enter in the field.

### `float` & `int` type

An `int` will not allow floating-point values to be entered from the website. A `float` will allow any number of decimal places.

```js
// float example:
{
    "type": "float",
    "label": "Master Mix Volume (uL)",
    "name": "master_mix_volume",
    "default": 20
}

// int example:
{
    "type": "int",
    "label": "Integer example",
    "name": "integer_example",
    "default": 10
}
```

### `dropDown` type

A `dropDown` will make a dropdown (aka `select`) UI widget.

Describe the `options` that are available in the dropdown by specifying the `label` (the text that the user sees) and the `value` (the text that `get_values('example_dropdown')` uses)

```json
{
  "type": "dropDown",
  "label": "Example Dropdown",
  "name": "example_dropdown",
  "options": [
    { "label": "Something here", "value": "aaa" },
    { "label": "Other thing", "value": "bbb" }
  ]
}
```

If the user selects "Other thing", `x = get_values('example_dropdown')[0]` will give you `x === "bbb"`.

Note that unlike other field types, `dropDown` has no `default`. Instead, it will always default to the first option.

### `textFile` type

This creates a file upload widget.

It's important for PL that you specify a working `default` value so that the protocol can by simulated using that default value.

```json
{
  "type": "textFile",
  "label": "Example file",
  "name": "example_file",
  "default": "1,2,3"
}
```

##### Common Use Case: CSV file upload

Here's a useful function for working with CSV files. Remember, the file will just be read as a string. It's up
to your protocol to parse that string into a useful data format.

```python
def well_csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list, re-ordering to match
    Opentrons API well order convention (A1, B1, C1, ..., A2, B2, B2, ...).

    The orientation of the CSV cells should match the "landscape" orientation
    of plates on the OT-2: well A1 should be on the top left cell. Example:

    A1, B1, C1, ...
    A2, B2, C2, ...
    A3, B3, C3, ...

    Returns a list: [A1, B1, C1, ..., A2, B2, C3, ...]
    where each CSV cell is a string in the list.
    """
    return [
        well for row in csv_string.split('\n') if row
        for well in row.split(',') if well]

def run(context):
    example_file = get_values('example_file')
    # pass the file contents string into this utility fn
    well_list = well_csv_to_list(example_file)
```

### Validation? Nope

Basic validation exists for `int` and `float` types, though it's possible to get the string `'NaN'`.

Field/form validation, such as setting min and max values, is not currently supported.

If any validation is necessary, add it in the protocol itself, eg:

```python
def run(context):
    some_field, other_field = get_values(  # noqa: F821
        'some_fields', 'other_field')
    assert some_field > 0
    assert other_field + some_field <= 96
    # et cetera

    # ... do stuff here ...
```

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
* A single `README.md` readme file
* A single `.py` [Opentrons protocol](http://docs.opentrons.com) file
* Optional "dot files" (see below)

## README file format

Every protocol should have a README file in its folder, with the file name `README.md`. It is a [Markdown](https://daringfireball.net/projects/markdown/syntax) file, with a specific format:

```markdown
# Human-Readable Protocol Name Here

### Author
[Your Name here](http://www.your.web.site.com/)

### Partner
[Partner Name here](https://www.example.com/)

## Categories
* Proteins & Proteomics
  * Assay

## Description
Describe and summarize the protocol here.
What is the purpose of the protocol?
What special labware is required?

### Time Estimate
30 minutes

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](https://opentrons.com/ot-one-hood)

### Modules
* [CoolDeck](https://shop.opentrons.com/collections/labware/products/cold-deck)

### Reagents
* ddH2O
* cDNA samples
* Et cetera

## Process
1. Describe the steps that a scientist takes to execute the protocol.
2. Put the steps in a numbered list
3. Et cetera

### Additional Notes
Notes here will show up on the bottom of the protocol on the website.

###### Internal
Notes here will not be published on the Opentrons Protocol Library website,
but will be visible in the public GitHub Protocols repo.
```

## "Dot files"

"Dot files" are files inside a protocol folder which start with a dot (`.`).

These files are usually blank text files. They have special names that indicate specific properties:

* `.feature` - The protocol will be listed under "Featured Protocols" on the website.
* `.ignore` - The protocol will not be shown on the Opentrons Protocol Library, even if you search for it.
* `.notests` - The protocol will not be tested by continuous integration. This is intended only for ignored protocols.
* `.embedded` - This is for "embedded apps" that generate a protocol and are designed to be shown in the Protocol Library in an iframe. This file should not be blank, it should contain a URL to the web app that will be embedded in the iframe.

# Custom Protocols

"Custom protocols" allow users to set variables for their protocol on the protocol library site before downloading a protocol,

## Writing Custom Protocols

### NOTE

Custom protocols is an early-stage feature, under active development. They are subject to change.

### Part 1: Set up containers + instruments

First, set up your containers and instruments normally at the top of the `.py` file.

For some protocols, you might want "number of destination plates" to be a variable. However, the deck map on the website is currently not dynamic - it will only show containers loaded at the top of the file. For this reason, you should load all the containers you might need at the top of the file, and then only use what you need during the actual execution.

### Part 2: Set your customizable arguments

To make a protocol customizable, put all your commands that run on the robot in a function called `run_custom_protocol`.

The arguments to that function will be used to create input forms on the Protocol Library website page for your protocol.

You can use [Python function annotations](https://www.python.org/dev/peps/pep-3107/) to specify what type of input to use. Right now, only `float` and `int` are supported.

Field names on the protocol's webpage will be named after the arguments. Eg, `number_of_samples: int=2` becomes `Number of samples` on the form, an integer field with a default of 2.

Form validation, such as setting min and max values, is not currently supported.

### Part 3: Commands

Inside your `run_custom_protocol` function, write all your robot commands (`transfer`, `distribute`, etc.)

## A simple example

Use a multi-channel pipette to transfer a custom number of rows from one plate to another, with a custom transfer volume

```python
from opentrons import instruments, containers

# set up containers and instruments

source = containers.load('96-flat', 'C1')
dest = containers.load('96-flat', 'E1')

trash = containers.load('trash-box', 'B2')
tiprack = containers.load('tiprack-200ul', 'A1')

p200_multi = instruments.Pipette(
    axis='a',
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=200,
    min_volume=20,
    channels=8,
)

# set up special `run_custom_protocol` function, with annotated arguments

def run_custom_protocol(transfer_volume: float=1.0, number_of_rows: int=1):
    # all commands go in this function
    p200_multi.distribute(
      transfer_volume,
      source.rows(0, to=number_of_rows),
      dest.rows(0, to=number_of_rows))

```

### Very Experimental: dropdown menus in custom protocols

#### StringSelection

Copy and paste this block near the top of your protocol.

```python
class StringSelection(object):
    def __init__(self, *containers):
        self.accepted_containers = containers

    def generate_options(self):
        def humanize(txt):
            return txt.replace('-', ' ').replace('_', ' ')

        return [
            {'value': option, 'text': humanize(option)}
            for option in self.accepted_containers]

    def get_json(self):
        # Of the form:
        # {type: 'StringSelection',
        # options: [{value: '96-flat', text: '96 flat'}, ...]}
        return {
            'type': 'StringSelection',
            'options': self.generate_options()}
```

Then use it in your `run_custom_protocol` function:

```python
def run_custom_protocol(
  well_volume: float=20.0,
  plate_type: StringSelection('96-flat', '96-PCR-tall', '96-deep-well')='96-flat',
  tuberack_type: StringSelection('tube-rack-.75ml', 'tube-rack-2ml')='tube-rack-.75ml'):

    plate = containers.load(plate_type, 'A1')
    tube_rack = containers.load(tuberack_type, 'C1')
    # do stuff with the plate here...
```

The line `plate_type: StringSelection('96-flat', '96-PCR-tall', '96-deep-well')='96-flat'` means:

* Create a dropdown selection menu called "Plate Type" with the options: '96-flat', '96-PCR-tall', '96-deep-well'
* The default value will be '96-flat' (from the `='96-flat'` at the end)

And another selector menu is made for "Tuberack Type" with options: 'tube-rack-.75ml', 'tube-rack-2ml'.

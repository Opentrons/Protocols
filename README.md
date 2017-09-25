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
* Proteins and Proteomics

### Sub Categories
*

## Description
Describe and summarize the protocol here.
What is the purpose of the protocol?
What special labware is required?

### Time Estimate
30 minutes

### Robot
* OT PRO
* OT Standard
* OT Hood

### Modules
* CoolDeck

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

* `.ignore` - The protocol will not be shown on the Opentrons Protocol Library, even if you search for it.
* `.feature` - The protocol will be listed under "Featured Protocols" on the website.
* `.embedded` - This is for "embedded apps" that generate a protocol and are designed to be shown in the Protocol Library in an iframe. This file should not be blank, it should contain a URL to the web app that will be embedded in the iframe.

# Writing Custom Protocols

TODO

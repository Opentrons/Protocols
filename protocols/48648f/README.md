# Nucleic acid purification from 90 patient samples

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Nucleic Acid Extraction & Purification
  * Nucleic Acid Purification

## Description
This protocol automates the transfer of 90 patient samples to an extraction plate for the purification of nucleic acids using an Opentrons OT-2 robot. This is a pythonized version of a [Protocol Designer protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-01-27/jd23jyu/Sample%20Plating%2090%20samples.json).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons P1000-single channel electronic pipettes (GEN2)](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 1000ul Filter Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-filter-tips)
* [Opentrons Temperature Module (GEN2)](https://shop.opentrons.com/products/tempdeck?_pos=1&_sid=5b80a3c66&_ss=r)
* [MTCbio 10 ml tube](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-01-27/jj43jf5/mtcbio_15_tuberack_10000ul.json)
* [NEST 96 2 mL](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-01-27/ox33jt1/nest_96_wellplate_2000ul.json)


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Setup up deck according to instructions.  Each of the six patient sample racks should contain a full set of 15 samples.  Wells A1, B1, H1, A7, B7, and H7 in the extraction plate are left empty. Transfers 100uL of each sample into a new well on the extraction plate using the custom tube rack and custom NEST well plate.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
48648f

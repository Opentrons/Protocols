# Functionalization of Electrodes

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
     * Plate Filling

## Description

This protocol uses a p20 single channel pipette to deposit Ag,AgCl, PVC membrane and an aqueous conditioning solution onto reference electrode bars and electrode wells of a custom 5 x 10 arrangement of electrode boards.

Links:
* [custom 5 x 10 arrangement Dimensions (offsets)](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-06-24/ao13rwm/Sensor%20V2%20Dimensions%20offsets.pdf)
* [custom 5 x 10 arrangement Dimensions (wells)](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-06-24/9t03rv3/Sensor%20V2%20Dimensions%20%26%20wells.pdf)
* [custom 5 x 10 arrangement Dimensions (well detail)](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-06-24/ax23rfl/Sensor%20V2%20Dimensions%20well.pdf)

This protocol was developed to deposit Ag,AgCl, PVC membrane and an aqueous conditioning solution onto reference electrode bars in three locations (end left, center, end right) and into electrode wells of a custom 5 x 10 arrangement of electrode boards according to the steps listed below.

## Protocol Steps

Set up: Custom electrode board arrangement in deck slot 1 (also occupying slots 2, 4 and 5). Reagent reservoir in slot 3 (A1- Ag,AgCl, A2-A5 PVC membrane, A6 reference PVC membrane, A7-A10 aqueous conditioning solution), p20 filter tips in slots 10 and 11.

The OT-2 will perform the following steps:
1. step 1- p20s deposit 40 ul Ag,AgCl at each location on each reference electrode bar- end(left), center, and end(right).
2. step 2- overnight delay for solvent evaporation.
3. steps 3 and 4- p20s deposit 10 uL PVC membrane into each 1st small well (first within the group of four), then each 2nd, each 3rd, and finally each 4th.
4. step 5- p20s deposit 30 uL reference PVC membrane on top of Ag/AgCl already deposited on the reference electrode bars in each of the three locations.
5. step 6- one hour delay for solvent evaporation.
6. step 7-  p20s deposit 30 uL aqueous conditioning solution into each 1st small well (first within the group of four), then 2nd, 3rd, 4th.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.19.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons Single-Channel p20 Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons Tips for the p20 pipette](https://shop.opentrons.com/collections/opentrons-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/71f107/layout_71f107.png)

* Opentrons p20 tips (Deck Slots 10, 11)
* custom 5 x 10 arrangement of electrode boards (Deck Slot 1-also occupies slots 2, 4 and 5)
* reagent reservoir nest_12_reservoir_15ml (Deck Slot 3)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Indicate the preferred location for "end dispenses" of Ag,AgCl and number of millimeters well bottom clearance (tip height above the well bottom) for the process steps using the parameters below.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
71f107

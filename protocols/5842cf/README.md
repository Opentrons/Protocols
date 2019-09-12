# Cherrypicking and Normalization with CSV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking
	* Normalization


## Description
With this protocol, the robot goes between two sample plates (1X plate and 1/10X plate) and transfers samples to a destination plate, based on the uploaded CSV file. The robot then dilutes the samples (based on the same CSV) in the destination plate with Tris-HCl to normalize the sample concentration.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P50 Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P10 Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [10uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 4-in-1 Tube Rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Bio-Rad Hard Shell 96-well PCR plate 200ul #hsp9601](bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* 50 mL Conical Tube

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Plate 1 (1X Plate): Slot 1

Plate 2 (1/10X Plate): Slot 3

Destination Plate: Slot 2

Tube Rack with Tris-HCl: Slot 5
	* Tris-HCl (in Conical Tube) should be placed in well 'A3'

10uL Tip Racks (x2): Slot 4, Slot 7

50/300uL Tip Racks (x2): Slot 6, Slot 9

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV (see below) and input protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
Note about the CSV: The CSV must be properly formatted in order for this protocol to run on the OT-2. The CSV should be formatted like so:

A1 | 1/10X | 5.6
A2 | 1X | 2.4
well | plate | volume

The first column will contain the wells and should be formatted `A1`, `B2`, `H12`, etc.

The second column should contain the name of the chosen sample (dilution) plate and for this protocol, should be either `1X` or `1/10X`.

The third column should contain the volume of Tris-HCl to be added to the destination plate to achieve the desired sample concentration. No cell should be blank ('0' if no Tris-HCl will be added).

Finally, there should be no headers in the CSV file.

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5842cf

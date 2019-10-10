# Protein Purification with MagDeck

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* Sample Prep


## Description
This protocol is designed to purify proteins from a 96-deep well block using a magnetic module. Plates will be supplied at the start of the protocol with bacterial lysate containing magnetic beads. The result will be a low volume 96-well plate containing purified protein. With this protocol, the user can choose how many samples they would like to run (1 - 96); the samples should be loaded sequentially starting at A1, then B1, etc. If running 48 samples or less, wash buffer should be loaded in to column 1 and 3, otherwise, columns 1-4 should be loaded with wash buffer (15mL).


---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette) or [P300 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* 96-Deep Well Plate, Porvair Sciences (no. 219027)
* 12-Column Reservoir, Porvair Sciences (no. 390005)
* 300mL Reservoir, Nalgene
* 96-Well V-Bottom Plate, Greiner
* Reagents
	* MagneHis Magnetic Beads
	* B-PER Complete Lysis Reagent
	* Wash Buffer
	* Elution Buffer


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 2: [300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 3: [300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 4: [300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 5: [300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 6: [300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 7: [300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 8: Greiner 96-Well V-Bottom Plate, clean and empty (for elution)

Slot 9: 12-Channel Reservoir, loaded (columns):
* Column 1: Wash Buffer (wash 1)
* Column 2: Wash Buffer (wash 1)
* Column 3: Wash Buffer (wash 2)
* Column 4: Wash Buffer (wash 2)
* Column 9: Elution Buffer

Slot 10: [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck) with Deep Well Plate, containing samples

Slot 11: 300mL Reservoir, empty (for liquid waste)



### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
65dc68

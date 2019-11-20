# MagBead Based Peptide Purification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
This protocol performs the [Zymo Zyppy-96 Plasmid MagPrep Kit](https://www.zymoresearch.com/collections/zyppy-plasmid-kits/products/zyppy-96-plasmid-magbead-kit). This protocols requires the use of the [P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette), [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck), and [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck). Users have the ability to set an incubation time (in minutes) for the step preceding the addition of the elution buffer (see below). The protocol begins with a 96-deep well plate, filled with 750µL of cell broth, placed on the Magnetic Module. The set up for the entire protocol can be found below.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons 300µL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Zymo Zyppy-96 Plasmid MagPrep Kit](https://www.zymoresearch.com/collections/zyppy-plasmid-kits/products/zyppy-96-plasmid-magbead-kit)
* Square 96-Deep Well Plates, 2.2mL ([Example](https://www.mt.com/us/en/home/products/pipettes/sample-preparation-tips/purespeed-accessories/LR-P2-96P-5.html))
* 12-Channel Reservoir ([Example](https://www.starlabgroup.com/en/consumables/robotic-tips_WebPSub-155854/84-ml-reservoir-multi-well-%7C-12-channel-%7C-high-profile_SLE2999-8412.html#tab=tecAttributes))
* Single-Channel Reservoir ([Example](https://www.mt.com/us/en/home/products/pipettes/high-throughput-platforms/accessories/LR-R2-PB-5.html))
* 96-Well Plate compatible with Temperature Module ([Example](https://lifescience.roche.com/en_us/products/lightcycler14301-480-multiwell-plate-96.html#overview))

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: Temperature Module with 96-Well Plate (empty, for final elution)

Slot 2: 12-Channel Reservoir (loaded)
* A1: Deep Blue Lysis Buffer
* A2: Deep Blue Lysis Buffer
* A3: ~Empty~
* A4: MagClearing Beads
* A5: ~Empty~
* A6: MagBinding Beads
* A7: ~Empty~
* A8: Endo-Wash Buffer
* A9: Endo-Wash Buffer
* A10: Endo-Wash Buffer
* A11: ~Empty~
* A12: Zyppy Elution Buffer

Slot 3: Single-Channel Reservoir (filled with Zyppy Wash Buffer)

Slot 4: Magnetic Module with 96-Deep Well Plate (filled with 750µL of cell broth to start)

Slot 5: 96-Deep Well Plate (clean and empty)

Slot 6: Single-Channel Reservoir (filled with Neutralization Buffer)

Slot 7: Single-Channel Reservoir (empty for liquid waste)

Slot 8: Opentrons Tiprack

Slot 9: Opentrons Tiprack

Slot 10: Opentrons Tiprack

Slot 11: Opentrons Tiprack

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
This protocol requires user intervention. Whenever user intervention is required, the robot will stop and a prompt with more instructions will appear in the OT app.

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
55f974

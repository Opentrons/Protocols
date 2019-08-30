# Sample Prep with Magnetic Beads

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
This protocol is used to aid in the prep for nucleic acid extraction. The robot begins by creating 3 separate wash plates and an elution plate. After loading a plate containing the samples, the robot adds isopropanol to each of the samples. The robot then adds magnetic beads to each sample. After the user washes the beads in each wash plate, the robot adds an elution buffer to the beads/sample mixture to release the DNA from the beads.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P50 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette?variant=5984202489885)
* [P300 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette?variant=5984202489885)
* [300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Bio-Rad Hard Shell 96-well PCR plate 200ul #hsp9601](bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* 96-well Square Plate

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: Empty 96-well plate (will become 'Wash 1')

Slot 2: Empty 96-well plate (will become 'Wash 2A')

Slot 3: Empty 96-well plate (will become 'Wash 2B')

Slot 4: 96-well plate with samples (added during the run)

Slot 5: 12-channel reservoir
* channel 1: Bead Mix
* channel 3: 100% Isopropanol
* channel 5: Wash Solution 1
* channel 7: Wash Solution 2
* channel 8: Wash Solution 2
* channel 10: DNA Elution Buffer 1
* channel 12: DNA Elution Buffer 2

Slot 6: Empty 96-well plate (will become 'Elution')

Slots 7-9: Tipracks for [P50](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette?variant=5984202489885)

Slots 10-11: Tipracks for [P300](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette?variant=5984202489885) 

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
599d38

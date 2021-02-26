# NGS Library Cleanup with Ampure XP Beads

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
	* Ampure XP

## Description
This protocol performs a custom NGS library cleanup using Ampure XP beads in a variable ratio with samples. The samples are mounted on an Opentrons magnetic module, and the final elute is transferred to a fresh PCR plate.

Explanation of complex parameters below:
* `park tips`: If set to `yes` (recommended), the protocol will conserve tips between reagent addition and removal. Tips will be stored in the wells of an empty rack corresponding to the well of the sample that they access (tip parked in A1 of the empty rack will only be used for sample A1, tip parked in B1 only used for sample B1, etc.). If set to `no`, tips will always be used only once, and the user will be prompted to manually refill tipracks mid-protocol for high throughput runs.
* `track tips across protocol runs`: If set to `yes`, tip racks will be assumed to be in the same state that they were in the previous run. For example, if one completed protocol run accessed tips through column 5 of the 3rd tiprack, the next run will access tips starting at column 6 of the 3rd tiprack. If set to `no`, tips will be picked up from column 1 of the 1st tiprack.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [NEST 12-channel reservoir 15ml #1061-8150](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)
* [P20 multi-channel electronic pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P300 multi-channel electronic pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 20ul filter tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-filter-tip)
* [Opentrons 200ul filter tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-200ul-filter-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 7)
* channel 1: Ampure XP beads
* channel 2: 80% ethanol
* channel 3: EB buffer
* channels 11-12: liquid waste (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P20 and P300 multi-channel pipettes and the number of samples to process.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
70567f

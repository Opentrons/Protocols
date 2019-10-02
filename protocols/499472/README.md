# Nucleic Acid Prep with MagBeads

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
This protocol performs a multi-step nucleic acid purification protocol that involves use of the [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck) and [Opentrons Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck). This protocol is designed for use with 96 samples and designed to pause for user inputs (adding reagents, replacing tipracks, etc). See the Setup section below for more details regarding the placement of reagents and labware.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P50 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P300 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [50/300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons Temperature Module with Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Bio-Rad Hard Shell 96-well PCR plate 200ul #hsp9601](bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Agilent 290ml Reservoir](https://labware.opentrons.com/agilent_1_reservoir_290ml)
* 2mL Tubes (preferably screwcap), for [Aluminum Tube Rack](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons Aluminum Tube Rack](https://shop.opentrons.com/collections/racks-and-adapters/products/aluminum-block-set)
	* A1: Hybridization Buffer (HB)
	* B1: Hybridization Buffer + Spike_1 (HB1)
	* C1: Magnetic Beads

Slot 2: 12-Channel Reservoir
	* Column 1: Reaction Buffer Master Mix
	* Column 2: HRP
	* Column 3: Substrate

Slot 3: 290ml Reservoir (loaded with PBS-T)

Slot 4: [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

Slot 5: 290ml Reservoir (empty, for liquid waste)

Slot 6: 290ml Reservoir (loaded with Wash Buffer)

Slot 7: [Opentrons Temperature Module with 96-Well Aluminum Block](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

Slot 8: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 9: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 10: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 11: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

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
499472

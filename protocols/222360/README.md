# NGS Cleanup with AMPure Magnetic Beads

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
With this protocol, you can perform nucleic acid purifications that are similar to the [NGS Cleanup and Size Selection with Omega Bio-Tek Mag-Bind TotalPure](https://protocols.opentrons.com/protocol/omega_biotek_magbind_totalpure_NGS) found in the [Opentrons Protocol Library](https://protocols.opentrons.com/) with slight modifications.

Updates to this protocol:

* A second trough for ethanol (column 2 and 3)
* Three troughs for liquid waste (columns 10, 11, and 12)
* Longer incubation and drying times
* Manual pause/resume steps after ethanol wash steps

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P50 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) (preferred, see Additional Notes below)
* [50/300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Bio-Rad Hard Shell 96-well PCR plate 200ul #hsp9601](bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* MagBeads (AMPure)
* Ethanol
* Elution Buffer (nuclease-free water)


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck) with Bio-Rad plate, containing samples

Slot 2: Bio-Rad plate, clean and empty (for elution)

Slot 3: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 4: Empty

Slot 5: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 6: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 7: 12-Channel Reservoir, loaded (columns):
* 1: MagBeads
* 2: Ethanol
* 3: Ethanol
* 4-9: Not Used
* 10: Empty (for Liquid Waste)
* 11: Empty (for Liquid Waste)
* 12: Empty (for Liquid Waste)

Slot 8: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 9: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 10: [50/300uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)


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
Note about pipettes: This protocol involves volume transfers below 30ul. Because of this, the P50-Multi and the P50-Single are highly recommended. The P300 pipettes can be used, but we cannot guarantee the accuracy of the aforementioned transfers.

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
222360

# Mass Spec Sample Prep

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* Sample Prep


## Description
This protocol is used for sample preparation with the Oasis Elution Plate. After each transfer, the robot will pause to allow the user to move the plate to a waste collection container. The protocol calls for the following transfers: MeOH (200uL), 0.1% Formic Acid in H2O (200uL), 5% MeOH in H2O (200uL), 26mM TFA in ACN (200uL), and 0.1% Formic Acid in H2O (500uL). See below for deck set-up.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons Multi-Channel Pipette, P50/P300](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette) or [Opentrons Single-Channel Pipette, P50/P300/P1000](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette) (Recommended: [P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885))
* [Opentrons 50uL/300uL Tips (if using P50/P300)](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 1000uL Tips (if using P1000)](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* Oasis HLB µElution Plate 30µm
* Analytical 170mL Reservoir
* Square 96-Well Collection Plates, 2mL
* Samples/Solutions/Reagents

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: Oasis µElution Plate

Slot 2: Analytical 170mL Reservoir (MeOH)

Slot 3: Analytical 170mL Reservoir (0.1% Formic Acid)

Slot 4: Analytical 170mL Reservoir (5% MeOH in H2O)

Slot 5: Analytical 170mL Reservoir (26mM TFA in ACN)

Slot 6: Empty

Slot 7: Opentrons Tiprack

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
067314

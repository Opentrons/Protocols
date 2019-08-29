# Tube Filling into 48-well or 24-well Tube Racks

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Distribution


## Description
This protocol allows your robot to transfer solution from a single source tube (15 mL or 50 mL Falcon conical tube) to up to nine 48-well or 24-well tube racks containing Sarstedt screw-cap tubes (either 0.5 mL, 1.5 mL or 2 mL).

User need to specify the following:
* Transfer Volume: volume to be transferred to each Sarstedt tube
* Tube Rack Type: tube rack format to be used to hold the Sarstedt tubes
* Tube Type: Sarstedt tube format to be used in the protocol
* Number of Racks: total number of Sarstedt tube racks to be filled
* Falcon Tube Type: source tube format
* Starting Stock Volume in mL: starting volume inside the Falcon tube
* Pipette Type: Single-channel Pipette to be used
* Pipette Mount: the side to which you wish to attach the above pipette
* Starting Tip: the tip to be used in the tip rack, pick from A1-H12

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* Custom 24-well Rack or Custom 48-well Rack
* Sarstedt Tubes 0.5 mL, 1.5 mL or 2 mL

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Opentrons 15x15 mL or 6x50 mL Tube Rack
* A1: Stock

24-well or 48 well Racks (starting from slot 2-10)
* Fill each entire rack with the desired tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
4a0be6

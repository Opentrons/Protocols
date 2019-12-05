# Sample Prep with CSV (updated)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* Sample Prep


## Description
**Note:** This is protocol is an updated version of [this protocol](http://protocol-delivery.protocols.opentrons.com/protocol/637687).

This protocol transfers a specific amount of a trypsin solution and an ABC solution to each well in a Eppendorf 96-well deep plate. To determine how much of each solution should be transferred to each well, a CSV is required that is formatted like so:

`Well` | `Trypsin Solution (30-300uL)` | `ABC Solution (100-1000uL)`

The CSV should include headers and be uploaded below. The protocol that is downloaded will make the transfers according to the CSV file. Find labware requirements and deck setup below.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons P300 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [Opentrons P1000 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [Opentrons 300uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 1000uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [Opentrons 4-in-1 Tube Rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 15mL Conical Tube
* 50mL Conical Tube
* Solutions
* Eppendorf 96-Well Deep Plate, 2mL

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons 1000uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

Slot 2: [Opentrons 300uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 4: Eppendorf Plate with samples

Slot 5: [Opentrons 4-in-1 Tube Rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* A1: Trypsin Solution (9000uL)
* A3: ABC Solution (45000uL)
* B3: ABC Solution (45000uL)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Upload CSV and input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
637687-v2

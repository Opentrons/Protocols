# BioFluid Transfer (Step 1)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Distribution


## Description
This protocol is designed for the high-throughput of biofluid from cryovial to centrifuge tube transfer. This protocol assumes that the cryovial rack has 50 samples and the centrifuge tube rack will be filled with the corresponding 50 samples. When transferring more than 50 samples, the operation will pause and the user will be prompted to replace the cryovials and centrifuge tubes on the deck.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* Cryovials (containing samples)
* 0.5mL centrifuge tubes (clean and empty)
* Custom container for holding cryovials
* Custom container for holding centrifuge tubes

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 2/5/8: Custom container for holding centrifuge tubes, filled with 0.5mL centrifuge tubes

Slot 3/6/9: Custom container for holding cryovials, filled with cryovials containing samples

Slot 1: [300ul Opentrons tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 4: [300ul Opentrons tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 7: [300ul Opentrons tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 10: [300ul Opentrons tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 11: [300ul Opentrons tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)


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
229e98

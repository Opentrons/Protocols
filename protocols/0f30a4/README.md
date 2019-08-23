# Sample Aliquoting

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Filling


## Description
This protocol performs custom sample aliquoting on 15ml tubes and a 4x6 10ml Agilent wellplate. Liquid height tracking is carried out on the 50ml water and scale control tubes to ensure the pipette is not contaminated. A dilution is carried out across each row of the Agilent wellplate to finish the protocol.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [P1000 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Agilent 24-well plate 10ml #202061-100](https://agilentmicroplates.com/products/202061-100/)
* [Opentrons 4-in-1 tuberack set](https://shop.opentrons.com/products/tube-rack-set-1)
* [15ml and 50ml conical Falcon tubes](https://ecatalog.corning.com/life-sciences/b2c/US/en/Liquid-Handling/Tubes,-Liquid-Handling/Centrifuge-Tubes/Falcon%C2%AE-Conical-Centrifuge-Tubes/p/falconConicalTubes)
* [Opentrons 300ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 1000ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

50ml tuberack:
* A1: water (tube 1)
* B1: water (tube 2)
* A2: scale control 1
* B2: scale control 2
* A3: scale control 3

12-channel reservoir:
* channel 1: solution 1
* channel 2: solution 2
* channel 3: solution 3
* channel 4: solution 4

15ml tuberack:
* all 15 wells of tuberack filled with empty 15ml falcon tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P1000 and P300 single-channel pipettes.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
0f30a4

# Checkerboard Assay

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Cell Culture
	* Assay

## Description
This protocol performs a custom checkerboard cell culture assay with 2 drugs at 8 different concentrations each from a stock deepwell plate across up to 6 culture plates. For a detailed workflow description, please download and view [this document](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2019-10-02/oe13q0g/protocol%20request%20cherckerboard.pdf)

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [USA Scientific 96-deepwell plate 2.4ml #1896-2000](https://www.usascientific.com/2ml-deep96-well-plateone-bulk.aspx)
* [Corning 96-flat well plate 360ul](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Corning%C2%AE-96-well-Solid-Black-and-White-Polystyrene-Microplates/p/corning96WellSolidBlackAndWhitePolystyreneMicroplates)
* [Opentrons 4-in-1 tube rack set with 50ml conical tube insert](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Falcon conical tubes 50ml #352070 (or equivalent)](https://ecatalog.corning.com/life-sciences/b2c/US/en/Liquid-Handling/Tubes,-Liquid-Handling/Centrifuge-Tubes/Falcon%C2%AE-Conical-Centrifuge-Tubes/p/falconConicalTubes)
* [P50 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [P300 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [Opentrons 300ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

2x3 50ml tuberack (slot 11):
* tube A1: water
* tube B1: growth medium

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P50 and P300 single-channel pipettes and the number of checkerboard plates (1-6).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
2780d4

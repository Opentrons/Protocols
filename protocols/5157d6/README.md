# Cell Culture Dilution

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Dilution


## Description
This protocol performs a custom cell culture dilution from one stock plate containing up to 8 drugs to up to 7 test plates. The user is prompted to refill reagents as necessary. The user can select whether the stock plate is a deepwell or a flat culture plate. The user can also allow for the following transfer parameters:
* which drug rows to select from the stock plate, separated by comma (example: `A,B,C,E,G`)
* number of test plates (up to 7)
* number of replicates per source for each test plate, aligned vertically in the corresponding column (example: for `3` replicates input, well A8 of the stock plate will be transferred to wells A8, B8, and C8 of each test plate)

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Corning 96-flat well plate 360ul](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Corning%C2%AE-96-well-Solid-Black-and-White-Polystyrene-Microplates/p/corning96WellSolidBlackAndWhitePolystyreneMicroplates)
* [USA Scientific 96-deepwell plate 2.4ml #1896-2000](https://www.usascientific.com/2ml-deep96-well-plateone-bulk.aspx)
* [Opentrons 15-tube rack 15ml](https://shop.opentrons.com/products/tube-rack-set-1)
* [P50 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [P300 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* TipOne 300ul tip racks

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

15ml tube rack
* A1: growth medium  
* A2: water

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mounts for your P300 and P50 single-channel pipettes, the stock plate type, the drug rows to replicate, the number of destination test plates, and then number of replicates per source well (for each test plate).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5157d6

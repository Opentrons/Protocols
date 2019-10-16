# Cytotoxicity Assay

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Cell Culture
	* Assay

## Description
This protocol performs a cytotoxicity assay and 1:2 dilution on a 96-well culture plate. Media and cells are contained in 50ml tubes. Aspiration heights for the 50ml tubes are automatically calculated during media and cell distribution to ensure the tip is submerged without contaminating the pipette. Heights are initialized assuming the 50ml tubes are filled to approximately 40ml.

Download and view [this file](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/3c12b0/cytotoxicity+assay+OT-2.xlsx) for a detailed workflow of the assay and dilution.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Corning 96-well flat culture plate 360ul](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Corning%C2%AE-96-well-Solid-Black-and-White-Polystyrene-Microplates/p/corning96WellSolidBlackAndWhitePolystyreneMicroplates)
* [Opentrons 4-in-1 tuberack set with 2x3 50ml tube insert](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Nest 50ml conical tubes](https://shop.opentrons.com/collections/verified-consumables/products/nest-50-ml-centrifuge-tube) (or equivalent, i.e. Falcon 50ml conical tubes)
* [Opentrons 300ul tiprack](https://shop.opentrons.com/collections/verified-consumables/products/opentrons-300ul-tips)
* [P300 electronic single-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

50ml tuberack (slot 1):
* tube A1: media (tube A)
* tube B1: effector cells (tube B)
* tube A2: control target cells (tube C)
* tube B2: target cells (tube D)
* tube A3: waste tube for extra volume from dilution (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P300 single-channel pipette.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
3c12b0

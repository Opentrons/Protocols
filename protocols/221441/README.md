# Cell Digestion and Labeling

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Cell Culture
	* Assay

## Description
This protocol performs cell digestion and labeling on a custom Corning HTS transwell plate.

**Important Note**: calibrate the Corning 96-well v-bottom plate _without_ the membrane insert. Height calculations for distribution from the 12-channel reservoir as well as for puncturing the membrane will be made accordingly.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons temperature module with 96-well aluminum block](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Corning HTS Transwell 96-well permeable support with 1.0 µm pore polyester membrane 360ul #3380](https://ecatalog.corning.com/life-sciences/b2c/US/en/Permeable-Supports/HTS/HTS-Transwell%C2%AE-96-well-Permeable-Support/p/3380)
* [Corning 96-well plate v-bottom 320ul #3894](https://ecatalog.corning.com/life-sciences/b2c/US/en/Permeable-Supports/Inserts/Corning%C2%AE-96-well-Clear-Polystyrene-Microplates/p/3894)
* [USA Scientific 12-channel reservoir #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons 96 Well Aluminum Block with Generic PCR Strip 200 µL](https://labware.opentrons.com/opentrons_96_aluminumblock_generic_pcr_strip_200ul?category=aluminumBlock)
* [P300 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [TipOne RPT low retention 10ul tips #1181-3810](https://www.usascientific.com/10ul-tipone-rpt-filtertip.aspx)
* [TipOne RPT low retention 300ul tips #1180-9810](https://www.usascientific.com/300ul-tipone-rpt-filtertip.aspx)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservor (slot 3)
* channel 1: solution for distribution

PCR strips in aluminum block (slot 5)
* strip column 1: solution for transfer

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P300 and P10 multi-channel pipettes, the number of sample columns to process (1-12), and the temperature module set temperature (in degrees C, 4-95).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
221441

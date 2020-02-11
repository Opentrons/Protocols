# Cherrypicking from .csv

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
This protocol performs a custom cherrypicking workflow from `.csv` file using custom filtertips. The `.csv` file should be formatted as follows, **including header line** (all empty lines are ignored):

```
source plate,source well,volume,destination plate,destination well,height offset from top of source well
1,A2,7,5,A4,-4
```

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [NEST 96 Well Plate 100 µL PCR Full Skirt](https://shop.opentrons.com/collections/verified-labware/products/nest-0-1-ml-96-well-pcr-plate-full-skirt)
* [Opentrons P20 GEN2 single-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Biotix 96 Filter Tiprack 10µl](https://biotix.com/products/utip-for-universal-pipettes/10-%ce%bcl-xl-racked-filtered-sterilized/)

---

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your `.csv` file and input the mount side for your P20 GEN2 single-channel pipette.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
2c81c0

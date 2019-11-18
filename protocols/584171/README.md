# PCR Mastermix Assay from .csv

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* PCR preparation

## Description
This protocol creates PCR master mix assay plates from 12 source tubes based on `.csv` file input as shown here:

```
Source,Destination Well,Transfer Amount,# of Transfers
tube 1,A3,240 ul,2
tube 1,B3,240 ul,2
tube 1,G9,240 ul,2
tube 1,H9,240 ul,2
tube 2,A4,240 ul,2
tube 2,B4,240 ul,2
tube 2,G8,240 ul,2
tube 2,H8,240 ul,2
tube 2,C6,240 ul,2
tube 2,D6,240 ul,2
tube 3,A5,240 ul,2
tube 3,B5,240 ul,2
tube 3,G7,240 ul,2
tube 3,H7,240 ul,2
tube 3,C7,240 ul,2
tube 3,D7,240 ul,2
tube 4,A6,240 ul,2
tube 4,B6,240 ul,2
```

You can also find a template file [here](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/584171/csv_template.csv). *Note: the file headers should be included, and empty lines are ignored.*

If more than one target assay plate is specified, the user is prompted to replace the completed plate with a new plate and to refill source PCR assay mix tubes mid-protocol.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [USA Scientific 96 Deep Well Plate 2.4ml #1896-2000](https://www.usascientific.com/2ml-deep96-well-plateone-bulk.aspx)
* [VWR 15ml conical centrifuge tubes #10025-686](https://us.vwr.com/store/product/12134703/vwr-centrifuge-tubes-with-flat-or-plug-caps-polypropylene-sterile-standard-line) or equivalent seated in [Opentrons 3x5 tuberack insert for 4-in-1 tuberack](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Opentrons GEN1 P300/P1000 electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 300/1000ul tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

3x5 15ml conical source tuberack (slot 1):
* *Ensure tubes are not filled above 11ml mark to prevent pipette contamination.*
![Tuberack setup](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/584171/tuberack.png)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input your single-channel pipette type, the mount side for your pipette, the input `.csv` file, and the number of target plates.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
584171

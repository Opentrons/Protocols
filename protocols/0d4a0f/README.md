# Cherrypicking

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
This protocol performs cherrypicking on a custom PCR plate. The protocol takes 2 `.csv` files as input-- one for the gblock setup, and one for the final water addition to equilize volumes. You can download templates for proper formatting here (*note-- headers should be included in both files*):
* [gblock template](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0d4a0f/gBlocks-Table+1.csv)
* [water template](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0d4a0f/Water-Table+1.csv)

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [USA Scientific Tempplate 96-well semi-skirted PCR plate 200ul #1402-9700](https://www.usascientific.com/semi-skirted-96-well-PCR-plate.aspx)
* [Tipone low retention 10ul tipracks](https://www.usascientific.com/10ul-tipone-rpt-wafers.aspx)
* [Opentrons 4-in-1 tiprack with 4x6 insert](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Nest 2ml screwcap tubes](https://shop.opentrons.com/collections/verified-consumables/products/nest-2-0-ml-microcentrifuge-tubes) or equivalent

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

4x6 tuberack (slot 4)
* tube A1: gibson assembly master mix
* tube B1: nuclease-free water

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P10 single-channel pipette, and your two `.csv` files.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
0d4a0f

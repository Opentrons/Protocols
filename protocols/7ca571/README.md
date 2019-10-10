# Heat Shock Transformation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Cell Culture
	* Assay

## Description
This protocol performs a custom heat shock transformation on up to 6 cell samples.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons 4-in-1 tuberack set (with 3x5 15ml Falcon tube insert for this protocol)](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Opentrons temperature module with aluminum block set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [P300 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [Opentrons 300ul tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 10ul tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

3x5 15ml Falcon tuberack (slot 1):
* tube A1: LB

4x6 aluminum block for 2ml Eppendorf tubes (slot 2); **cool to 4˚C before placing samples and running the protocol**:
* row A: up to 6 1.5ml Eppendorf tubes containing cells to receive corresponding DNA from row B
* row B: up to 6 1.5ml Eppendorf tubes containing starting DNA samples to be transferred to row A

8x12 aluminum block on temperature module for 42˚C heat shock (slot 4)
* empty PCR plate for heat shock transfer

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P300 and P10 single-channel pipettes, the number of samples to run (1-6), DNA volume (in µl), cell volume (in µl), and starting volume of LB in the 15ml Falcon tube (in ml, for accurate height tracking).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
7ca571

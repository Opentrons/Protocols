# Covid-19 qPCR Prep (Station C)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Covid-19 Workstation
	* Station C: qPCR Setup


## Description
This protocol creates a custom qPCR prep protocol for Covid-19 diagnostics. The input into this protocol is an elution plate of purified RNA, and the output is a PCR plate containing the samples mixed with mastermix.
Using a [Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette), this protocol will begin by creating reaction mix in a 2ml tube. The mix is then distributed to a PCR strip. Then, using the [Multi-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette), samples will be transferred from their plate to the qPCR plate and mixed with the reaction mix.

If you have any questions about this protocol, please email our Applications Engineering team at [protocols@opentrons.com](mailto:protocols@opentrons.com).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.21.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) with [Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set))
* [Opentrons P300 Single-Channel GEN2 Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P20 Multi-Channel GEN2 Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons Filter Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [NEST PCR Plate](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt) containing purified nucleic acid samples
* [2ml NEST screwcap tubes or equivalent](https://shop.opentrons.com/collections/tubes/products/nest-microcentrifuge-tubes) containing reaction mix(es)


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

chilled 24-well aluminum block for 2ml tubes (slot 5):
* well A1: mastermix tube (loaded empty)
* wells A2-D2: mastermix reagents in order listed by kit (2-4, depending on which kit is selected)


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Download your protocol bundle.
2. Upload [custom labware definition](https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols), if needed.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tipracks, and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
1ccd23

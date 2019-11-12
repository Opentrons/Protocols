# Nucleic Acid Purification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification

## Description
This protocol performs a custom nucleic acid purification protocol on a PCR plate mounted on an Opentrons magnetic module. Purified samples are transferred to a second elution plate.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Eppendorf twin.tec 96-well PCR plate 150ul #951020401](https://online-shop.eppendorf.us/US-en/Laboratory-Consumables-44512/Plates-44516/Eppendorf-twin.tec-PCR-Plates-PF-8180.html?_ga=2.82294422.1036747619.1572381519-1620298314.1562620987)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons magnetic module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons P50 multi-channel pipette (GEN1)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [Opentrons 300ul tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 4)
* channel 1: beads
* channels 2-3: 80% EtOH
* channel 4: elution buffer
* channels 11-12: liquid waste (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P50 muli-channel pipette and the number of samples to process.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
44306d

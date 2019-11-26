# Production of Biological Products

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Distribution

## Description
This protocol performs a custom protocol for production of biological products by distributing solution from a reservoir to up to 9 custom 48-disc plates with offset disc locations.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P300 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [Agilent single-channel reservoir 290ml #201252-100](https://www.agilent.com/store/en_US/Prod-201252-100/201252-100)
* Eppendorf epT.I.P.S. 96-tip Rack

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

290ml reservoir (slot 2)
* solution A

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P300 single-channel pipette, the number of plates, the number of discs per plate to receive solution, the volume to fill each disc (in ul), the transfer plan (distribution or single transfers), and the tip well (A1-H12).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
32b6ed

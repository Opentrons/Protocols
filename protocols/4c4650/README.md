# CSV Dilution

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Dilution


## Description
This protocol performs a custom CSV dilution from a custom gallipot containing diluent to up to 8 custom 6x8 2ml tube rack containing different primers. The input CSV file should contain volumes on separate lines, without a header, as shown in the following format:
```
1668
1665
1747
1759
1639
1682
1898
```

Every transfer uses a new tip to avoid contamination. Tubes are filled down each column before moving across (A1-F1, then A2-F2, etc.). Dispense offset (height below the top of the destination tube) is determined automatically to accommodate high volumes. The user is prompted to refill 1000ul tip racks as necessary throughout the protocol.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* custom Gallipot containing 1X tris-EDTA buffer
* custom 6x8 2ml tube racks containing primers
* [P1000 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 1000ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your volumes CSV formatted as specified above, and input the mount side for your P1000 single-channel pipette.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
4c4650

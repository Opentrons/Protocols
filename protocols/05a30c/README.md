# Spheroid Transfer

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Cell Culture
	* Assay

## Description
This protocol performs a custom spheroid transfer protocol from InSphero Akura 96-well to 384-well plates. For specific transfer scheme, see 'Additional Notes' below.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* Insphero Akura 96-well microtiter plates
* Insphero Akura 384-well flow plates
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [P300 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 300ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 6):
* channel 1: serum
* channel 2: wash buffer

300ul tiprack (slot 9), **calibrate to tip A1 even though row A does not contain tips**:
* rows A, G, and H: empty
* rows B-F: tips in all columns (1-12)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P300 multi-channel pipette, the aspirate and dispense flow rates (in ul/sec), and the spheroid release waiting time (in seconds).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
Transfer Scheme
![Transfer scheme](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/05a30c/transfer_scheme.png)

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
05a30c

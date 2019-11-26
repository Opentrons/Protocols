# DNA Normalization and Pooling from .csv

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
This protocol performs a custom protocol for cherrypicking, normalization, and pooling up to 96 DNA samples as specified in a `.csv` file. The file should be formatted as follows (with header line; empty lines are ignored):
```
source well,destination well,vol sample (ul),vol buffer (ul),pool vol (ul, 0 if no pooling)
A1,A1,5,5,8
C1,B1,2,8,4
```

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Bio-Rad Hardshell 96-well PCR plate 200ul #hsp9601](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons 4-in-1 tuberack](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1) with 4x6 microcentrifuge tube insert
* [Opentrons GEN1 P10/P50 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes)
* [Opentrons 10/300ul tipracks](https://shop.opentrons.com/collections/opentrons-tips)
* [1.5ml NEST snapcap microcentrifuge tube](https://shop.opentrons.com/collections/verified-consumables/products/nest-microcentrifuge-tubes) or equivalent

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 1):
* channel 1: buffer for normalization

Opentrons 4-in-1 tuberack with 4x6 microcentrifuge tube insert (slot 6)
* tubes A1: 1.5ml tube for pooling

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P10 single-channel pipette, and upload your `.csv` file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal

# Nucleic Acid Purification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
This protocol performs nucleic acid purification on a magnetic module. A temperature module is also on the deck and cools 41C for mid-protocol incubation. The user is prompted to replace tipracks, and to fill/empty channels in the reagent reservoir throughout the protocol to optimize deck space.

Initial HB distributions are uploaded in a csv as formatted in [this template](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5c6979/HB_layout.csv). The file should be uploaded as the `HB CSV` variable below.

Replicate columns for bead and reagent steps are uploaded in a CSV, with each line containing comma-separated replicate column numbers (1-12).  Empty lines are ignored. For example, if columns 1, 3, 4 contain sample replicates of the same type, columns 2 and 5 contain sample replicates of the same type, column 7 contains unique samples, and columns 6 and 8-12 are empty, the following CSV should be uploaded as the `Replicate CSV` variable below:

```
1, 3, 4
2, 5
7
```

The same tips will be used for steps performed on columns listed together in the CSV file to conserve tips.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P300 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [P50 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Bio-Rad Hardshell 96-well PCR plate low profile #hsp9601](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Agilent 1-channel reservoir 290ml](https://www.agilent.com/store/en_US/Prod-201252-100/201252-100)
* [Opentrons 4x6 aluminum block for 2ml screwcap tubes](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Opentrons 300ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

4x6 aluminum tuberack for 2ml screwcap tubes:
* A1: HB
* B1: HB1
* C1: HB2
* D1: HB3
* A2: magnetic beads

12-channel reservoir:
* channel 1: reaction buffer master mix
* channel 2: HRP
* channel 3: substrate (user prompted to load mid-protocol)
* channels 5-12: liquid waste (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P50 and P300 multi-channel pipettes, and upload your CSV file specifying replicate locations.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5c6979

# NEB Next Ultra II FS Library Prep: Size Selection of Adapter-ligated DNA

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* NGS Library Prep


## Description
This protocol performs the 'Size Selection of Adapter-ligated DNA' section of the [NEB Next Ultra II FS Library Prep protocol](https://www.neb.com/protocols/2017/10/25/protocol-for-use-with-inputs-greater-100-ng-e7805-e6177).

Links:
* [Adaptor Ligation](./68b326-adapter-ligation)
* [Size Selection of Adaptor-ligated DNA](./68b326-size-selection)
* [Cleanup of PCR Reaction](./68b326-cleanup-pcr)

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons magnetic module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Bio-Rad Hard Shell 96-well high profile PCR plate 350ul #hss9601](https://www.bio-rad.com/en-us/sku/hss9601-hard-shell-96-well-pcr-plates-high-profile-semi-skirted-clear-clear?ID=hss9601)
* [Axygen 12-channel reservoir 22ml #RES-MW12-HP](https://ecatalog.corning.com/life-sciences/b2c/US/en/Genomics-%26-Molecular-Biology/Automation-Consumables/Automation-Reservoirs/Axygen%C2%AE-Reagent-Reservoirs/p/RES-MW12-HP)
* [P50 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes)
* [P300 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes)
* [300ul Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 4)
* channels 1-2: 80% ethanol
* channel 3: 0.1X TE
* channel 5: SPRI beads
* channels 10-12: liquid waste (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount sides for your P50 and P300 pipettes and the number of samples to process.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
68b326

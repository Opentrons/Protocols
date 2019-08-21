# Oxford Nanopore 16S Barcoding NGS Library Prep

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* NGS Library Prep


## Description
This protocol performs the [Oxford Nanopore 16S Barcoding NGS library prep kit](https://community.nanoporetech.com/protocols/16S-barcoding-1-24/checklist_example.pdf).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P10 Single-channel electronic pipettte](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [P300 Single-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [Bio-Rad Hard Shell 96-well PCR plate 200ul #hsp9601](bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Opentrons 4-in-1 tuberack set(1.5ml Eppendorf snapcap top)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1
* [Axygen 12-channel reservoir 22ml #RES-MW12-HP](https://ecatalog.corning.com/life-sciences/b2c/US/en/Genomics-%26-Molecular-Biology/Automation-Consumables/Automation-Reservoirs/Axygen%C2%AE-Reagent-Reservoirs/p/RES-MW12-HP)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 3)
* channel 1: Ampure XP beads
* channel 2-3: EtOH
* channels 10-12: liquid trash (loaded empty)

1.5ml tuberack (slot 6)
* A1: nuclease-free water
* B1: LongAmp Hot Start Taq 2x mastermix
* A2: 10 mM Tris-HCl pH 8.0 with 50 mM NaCl
* B2: RAP

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the number of samples to process, the barcode start well, and the respective mount sides for your P10 and P300 single-channel pipettes.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
2a4397

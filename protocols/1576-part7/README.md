# Cell3™ Target Cell Free DNA Target Enrichment for NGS Part 7: Probe Capture on Streptavidin Beads and Washes

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* NGS Library Prep
    * Cell3™ Target

## Description
Links:
* [Part 1: Fragmentation / End-repair / A-tailing](./1576-part1)
* [Part 2: Ligation of Illumina UMI adapters](./1576-part2)
* [Part 3: Clean-up of adapter ligated library](./1576-part3)
* [Part 4: Library Amplification](./1576-part4)
* [Part 5: Library Pooling](./1576-part5)
* [Part 6: Probe Hybridization](./1576-part6)
* [Part 7: Probe Capture on Streptavidin Beads and Washes](./1576-part7)
* [Part 8: Captured Library Amplification and Clean-up](./1576-part8)

---
---

This protocol performs the workflow of Cell Free DNA Target Enrichment as described in the [NONACUS Cell3™ Target Protocol Guide v1.2.2](https://nonacus.com/wp-content/uploads/2019/05/Cell3Target_Protocol_v1.2.2.pdf). This particular section is part 7 of the series, capturing the biotin-labelled probes hybdrized to their DNA targets using Streptavidin beads. The beads are then washed to remove non-targeted DNA.

Note:
* Preparation of Wash Buffers and Dynabeads® M-270 Streptavidin are not included and must be performed off the robot prior to running this protocol

Before you start, review the protocol guide to confirm kit contents and make sure you have the required equipment and consumables. Follow the instructions to set up the appropriate thermocycler program. See 'Additional Notes' below for reagent setup.

After the protocol completes, place the Bio-rad Hardshell plate in the pre-heated thermocycler (95°C) and skip to the next step in the program. Leave the hybridization reaction mix at 65°C on the thermocycler to incubate for 4 hours.

---
---

You will need:

* [Opentrons P50 Single-channel Pipette](https://shop.opentrons.com/collections/hardware-modules/products/single-channel-electronic-pipette?variant=5984549077021)
* [Opentrons P300 Single-channel Pipette](https://shop.opentrons.com/collections/hardware-modules/products/single-channel-electronic-pipette?variant=5984549109789)
* [Opentrons 300 uL Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Biorad Hard-Shell 96-well PCR Plates](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Opentrons Temperature Module](https://shop.opentrons.com/products/tempdeck)
* [Opentrons Magnetic Module](https://shop.opentrons.com/products/magdeck)
* [Cell3™ Target: Library Preparation kit](https://nonacus.com/cell3tm-target/)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".

### Additional Notes
Reagent Setup:

![setup](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1576/reagent_setup_part7.png)


---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Lcy03lF7
1576

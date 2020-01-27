# Swift 2S Turbo DNA Library Kit Protocol: Part 3/3 - Indexing PCR & Final Clean-Up

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
	* Swift 2S Turbo


## Description
Part 3 of 3: Indexing PCR & Final Clean-Up

With this protocol, your [OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2) can perform the [Swift 2S Turbo DNA Library Kit](https://swiftbiosci.com/swift-2s-turbo-dna-library-kits/). For more information about the Swift 2S Turbo Kit on the OT-2, please see our white paper here: [Rapid high quality next generation sequencing library preparation with Swift 2S Turbo DNA Library Kits on the Opentrons OT-2](https://opentrons-landing-img.s3.amazonaws.com/bundles/fully_automated_ngs_application_note.pdf) 

In this part of the protocol, your [OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2) will complete the indexing portion of the protocol as outlined in the [Swift 2S Turbo Kit Guide](https://swiftbiosci.com/wp-content/uploads/2019/11/PRT-001-2S-Turbo-DNA-Library-Kit-Rev-1.pdf).

At the completion of this step, you will have 20μl of supernatant from each sample that contains the final library.

Links:
* [Part 1: Enzymatic Prep & Ligation](http://protocols.opentrons.com/protocol/swift-2s-turbo-pt1)
* [Part 2: Ligation & Indexing PCR](http://protocols.opentrons.com/protocol/swift-2s-turbo-pt2)
* [Part 3: Indexing PCR & Final Clean-Up](http://protocols.opentrons.com/protocol/swift-2s-turbo-pt3)


---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.15.0 or later)](https://opentrons.com/ot-app/)
* [Swift 2S Turbo DNA Library Kit](https://swiftbiosci.com/swift-2s-turbo-dna-library-kits/)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette)
* [Opentrons Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [Aluminum Block Set](https://shop.opentrons.com/collections/racks-and-adapters/products/aluminum-block-set)
* [NEST 96-Well PCR Plate, Full Skirt](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt)
* [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/reservoirs/products/nest-12-well-reservoir-15-ml)
* Samples


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: **Not used in this part** [Opentrons Temperature Module with 24-Well Aluminum Block](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) and 2mL Tubes
* A1: Enzymatic Prep Master Mix
* A2: Ligation Master Mix
* A3: Indexing PCR Master Mix


Slot 2: [NEST 12-Well Reservoir](https://shop.opentrons.com/collections/reservoirs/products/nest-12-well-reservoir-15-ml)
* A1: Magnetic Beads
* A3: **Not used in this part** 80% Ethanol Solution, Freshly Prepared
* A4: 80% Ethanol Solution, Freshly Prepared
* A6: Low EDTA TE Buffer


Slot 3: [NEST 96-Well PCR Plate](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt) on top of [96-Well Aluminum Block](https://shop.opentrons.com/collections/racks-and-adapters/products/aluminum-block-set) with samples
* 8 Samples: Column 1
* 16 Samples: Column 1 & Column 2


Slot 4: [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck) with [NEST 96-Well PCR Plate](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt)


Slot 5: **Not used in this part** [Opentrons Tips for Single-Channel Pipette](https://shop.opentrons.com/collections/opentrons-tips)


Slot 6: [Opentrons Tips for P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/opentrons-tips)


Slot 9: [Opentrons Tips for P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/opentrons-tips)


**Using the customizations fields, below set up your protocol.**
* **P300 Multi-Channel Pipette Tip Type**: Select which tips (filter/non-filter) to be used for this protocol.
* **Number of Samples**: Specify the number of samples (8 or 16) you'd like to run.


**Note:** The final elution will be transferred to column 3 (and column 4, if running 16 samples) of the PCR plate in slot 3.


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
Swift-2S-Turbo-pt3

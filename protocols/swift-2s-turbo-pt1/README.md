# Swift 2S Turbo DNA Library Kit Protocol: Part 1/3 - Enzymatic Prep & Ligation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
	* Swift 2S Turbo


## Description
Part 1 of 3: Enzymatic Prep & Ligation


With this protocol, your [OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2) can perform the [Swift 2S Turbo DNA Library Kit](https://swiftbiosci.com/swift-2s-turbo-dna-library-kits/). For more information about the Swift 2S Turbo Kit on the OT-2, please see our white paper here: [Rapid high quality next generation sequencing library preparation with Swift 2S Turbo DNA Library Kits on the Opentrons OT-2](https://opentrons-landing-img.s3.amazonaws.com/bundles/fully_automated_ngs_application_note.pdf)


In this part of the protocol, your OT-2 will complete the enzymatic prep portion and the initial steps of the ligation portion prior to adding your samples to a thermocycler, as described in the [Swift 2S Turbo Kit Guide](https://swiftbiosci.com/wp-content/uploads/2019/11/PRT-001-2S-Turbo-DNA-Library-Kit-Rev-1.pdf).


At the completion of this step, you will add your samples to the thermocycler and upon completion of thermocycle, continue with [Part 2 of the protocol](http://develop.protocols.opentrons.com/protocol/swift-2s-turbo-pt2).


Links:
* [Part 1: Enzymatic Prep & Ligation](http://develop.protocols.opentrons.com/protocol/swift-2s-turbo-pt1)
* [Part 2: Ligation & Indexing PCR](http://develop.protocols.opentrons.com/protocol/swift-2s-turbo-pt2)
* [Part 3: Indexing PCR & Final Clean-Up](http://develop.protocols.opentrons.com/protocol/swift-2s-turbo-pt3)




---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.15.0 or later)](https://opentrons.com/ot-app/)
* [Swift 2S Turbo DNA Library Kit](https://swiftbiosci.com/swift-2s-turbo-dna-library-kits/)
* [Opentrons Temperature Module with Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Opentrons P20 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette) or Opentrons P50 Single-Channel Pipette
* [Opentrons Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [NEST 96-Well PCR Plate, Full Skirt](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt)
* 2mL Tubes
* Samples



---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons Temperature Module with 24-Well Aluminum Block](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) and 2mL Tubes
* A1: Enzymatic Prep Master Mix
* A2: Ligation Master Mix


Slot 3: [NEST 96-Well PCR Plate](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt) on top of [96-Well Aluminum Block](https://shop.opentrons.com/collections/racks-and-adapters/products/aluminum-block-set) with samples
* 8 Samples: Column 1
* 16 Samples: Column 1 & Column 2


Slot 5: [Opentrons Tips](https://shop.opentrons.com/collections/opentrons-tips)




__Using the customizations fields, below set up your protocol.__
* **Single-Channel Pipette**: Select which pipette (P50 Single-Channel or P20 Single-Channel) to be used for this protocol. **The pipette should be attached to the left mount.**
* **Single-Channel Pipette Tip Type**: Select which tips (filter/non-filter) to be used for this protocol.
* **Number of Samples**: Specify the number of samples (8 or 16) you'd like to run.




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
Swift-2S-Turbo-pt1

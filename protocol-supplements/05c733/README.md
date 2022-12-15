# EmbgenixTM PGT-A Kit: Preparation of Whole Genome Amplification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
  * EmbgenixTM PGT-A

## Description

This protocol performs the [EmbgenixTM PGT-A Kit: Preparation of Whole Genome Amplification](https://www.takarabio.com/documents/User%20Manual/Embgenix%20PGT/Embgenix%20PGT-A%20Kit%20%28RUO%29%20User%20Manual%20for%20Illumina%20MiSeq%20System.pdf), parts V-VI:B.

### Modules
* [Opentrons Temperature Module (GEN2)](https://shop.opentrons.com/temperature-module-gen2/)

### Labware
* [Opentrons 96 Well Aluminum Block with NEST Well Plate 100 μL](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Opentrons 24 Tube Rack with Eppendorf 1.5 mL Safe-Lock Snapcap](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)

### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/05c733/deck.png)

### Reagent Setup
![reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/05c733/reagents.png)  
* Columns 1-2 on Temperature Module Plate (slot 7): Starting sample
* A1 on Tuberack (slot 4): Cell Extraction Master Mix
* B1 on Tuberack (slot 4): Whole Genome Amplification Master Mix
* C1 on Tuberack (slot 4): WD2
* D1 on Tuberack (slot 4): WD2
* A2 on Tuberack (slot 4): Library Prep Master Mix
* B2 on Tuberack (slot 4): Library Amplification Master Mix
* Columns 5-6 on Mix Distribution Plate (slot 5): Stem Loop Adapters
* Columns 1-2 on UDI Plate (slot 6): UDI

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit "Run".


### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
05c733

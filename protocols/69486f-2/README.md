# NGS Library Prep - Protocol 1


### Author
[Opentrons](https://opentrons.com/)


## Categories
* NGS Library Prep
	* KAPA HiFi


## Description

This custom protocol performs part 1 of the [KAPA HiFi NGS Library Prep kit](https://sequencing.roche.com/en/products-solutions/products/sample-preparation/library-amplification/kapa-hifi-kits.html). The operator is prompted to perform manual steps throughout the protocol.

### Modules
* [Opentrons Magnetic Module (GEN2)](https://shop.opentrons.com/magnetic-module-gen2/)


### Labware
* Agilent 3 Reservoir 94630 µL #204249-100
* KingFisher 96 Deep Well Plate #95040450
* Agilent 96 Well Plate 200 µL #401490
* Opentrons 96 Filter Tip Rack 20 µL
* Opentrons 96 Filter Tip Rack 200 µL
* [Opentrons 24 Tube Rack with Eppendorf 1.5 mL Safe-Lock Snapcap](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)


### Pipettes
* [Opentrons P20 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Opentrons P300 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/69486f-2/deck.png)


### Reagent Setup
Tuberack:  
![reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/69486f-2/reagents.png)  
* A1: mastermix tube
* B1: water
* C1: buffer 3
* D1: buffer 4
* A2: primer 1
* B2: primer 4


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
69486f-2

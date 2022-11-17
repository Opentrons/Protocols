# Custom Acid Digestion Assay Day 2


### Author
[Opentrons](https://opentrons.com/)


## Categories
* Sample Prep
	* Specific Category


## Description
This protocol is day 2 of a specialized assay. Samples and standards are added in triplicate from a custom aluminum
vial holder to a quartz reaction vessel. After a 1 hour wait, deionized water and three different reagents are added as needed to all samples and standards.


### Labware
* [NEST 12 Well Reservoir 15 mL #360102](http://www.cell-nest.com/page94?_l=en&product_id=102)
* Custom Aluminum Vial Holder
* [Zinsser Quartz 96 Well Plate](https://www.zinsserna.com/reactor_plates.htm)
* [Opentrons 96 Tip Rack 20 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 96 Tip Rack 300 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)


### Pipettes
* [Opentrons P20 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Opentrons P300 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/072463/deck.png)
NOTES ON SETUP:
* Temperature module will only be loaded onto the deck if set below in the variables
* Tiprack in slot 7 will change between 20 uL and 300 uL tips when transfer volume is set above or below 20 uL. Please double check in the Opentrons app when preparing the deck setup.
* Standards are in the first seven wells of the listed plate, A1-B3. Only two are listed to show well order. This also applies to samples. They will populate top to bottom, left to right, from A1, A2, A3, A4, B1, B2, etc.


### Reagent Setup
![reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/072463/reagents.png)


### Protocol Steps
0. If temperature module is being used, it pre-heats to 95 C
1. Samples are added in triplicate to the 96 well quartz plate from vials held in the custom aluminum plate. Volume is
determined by the volume variable below.
2. 36 uL deionized water is added to wells that will hold the standards
3. Standards are added in triplicate to the 96 well quartz plate from vials held in the custom aluminum plate. Volume is determined by the volume variable below.
Note: Standards are added to the wells immediately after the sample wells. E.g. if 4 samples are selected, wells A1-A12
will have samples in triplicate and wells B1-C9 will have 7 standards in triplicate
4. A 60 minute delay occurs, if the temperature module is being used it will heat to 95
5. 46 uL of deionized water is added to all wells in the quartz plate
6. 30 uL of Reagent A is added to all wells in the quartz plate
7. 49 uL of Reagent B is added to all wells in the quartz plate
8. 75 uL of Reagent C is added to all wells in the quartz plate


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
072463

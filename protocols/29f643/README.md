# Alpco Human Insulin ELISA


### Author
[Opentrons](https://opentrons.com/)


## Categories
* Sample Prep
	* ELISA


## Description
This protocol automates the Alpco Insulin ELISA protocol. The protocol begins by transferring aliquots of samples, standards, and controls. The rest of the protocol can be automated or include manual interventions (for wash steps and off-deck incubations). Please note this protocol is currently being optimized.

Explanation of complex parameters below:
* **Number of Samples**: Specify the number of samples
* **P300 Multi-Channel Mount**: Select which mount the P300 Multi-Channel Mount is attached to
* **Manually Add Controls**: Specify whether or not to manually add controls and standards
* **Perform Manual Washes**: Specify whether to perform wash steps manually or on the OT-2


### Labware
* [NEST 12 Well Reservoir 15 mL #360102](http://www.cell-nest.com/page94?_l=en&product_id=102)
* [NEST 96 Well Plate 100 µL PCR Full Skirt #402501](http://www.cell-nest.com/page94?_l=en&product_id=97&product_category=96)
* [NEST 1 Well Reservoir 195 mL #360103](http://www.cell-nest.com/page94?_l=en&product_id=102)
* [Opentrons 96 Tip Rack 300 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)


### Pipettes
* [Opentrons P300 8 Channel Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/29f643/deck.png)


### Reagent Setup
![reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/29f643/reagents.png)


### Protocol Steps
1. Transfer of 25µL of Standards and Controls into column 1 of the Destination Plate. Followed by 25µL aliquots of samples into two columns for each column of samples.
2. 100µL of Detection Antibody is added to Destination Plate.
3. User is prompted to remove plate from OT-2 and place on shaker for 1 hour incubation.
4. If automating washes, the OT-2 will add 350µL to all wells, then transfer 375µL to the liquid waste reservoir.
5. 100µL of TMB Substrate is added to the Destination Plate.
6. User is prompted to remove plate from OT-2 and place on shaker for 15 minute incubation.
7. 100µL of Stop Solution is added to the Destination Plate.
8. Protocol complete.


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
29f643

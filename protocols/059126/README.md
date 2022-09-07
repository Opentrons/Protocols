# Reagent Addition

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Reagent Addition

## Description
This is a specialized reagent addition to add reagent from vials in a Cytiva well plate to a 96 well plate which are then transferred to a 384 well plate. The tips are picked up in a non-standard manner with a single tip picked up from the bottom-right corner to add from the vials to the 96 well plate. The columns of the 96 well plate will then have a specified amount of each column added to the 384 well plate, reusing tips as much as possible.

Sample numbers should be specified in multiple of 16 for most efficient reagent use. I.e. 2 samples can be specified but reagent will be added to all of column 1 in the 384 well plate. 32 samples will add reagent to column 1 and 2 in the 384 well plate.

Explanation of complex parameters below:
* `Number of Samples in 384 Well Plate`: How many samples will be in the 384 well plate
* `Transfer Volume (1-20uL)`: How much liquid will be transferred from the 96 well plate to the 384 well plate in uL. Please keep in mind the max volume of 50uL for the 384 well plate when specifying number of vials and transfer volume along with the liquid handling in the script. I.e. During the 384 well addition, a blow-out followed by a tip touch will occur 1 mm below the well top to ensure no liquid remains in the tip or beads on the tip.
* `Number of Vials (1-12)`: How many starting vials are there in the Cytiva well plate. Each vial will fill a single column in the 96 well plate. A1 goes to column 1, B1 to column 2, C1 to column 3, etc.
*`P20 Multi GEN2 Mount`: Which mount the P20 multi-channel is connected to. The P300 will be connected to the opposite mount.  

---

### Labware
* Greiner 96 Well Plate 340uL
* Greiner 384 Well Plate 50uL
* Cytive 24 Well Plate 2000uL used as Vial Holder

### Pipettes
* [Opentrons P300 8 Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [Opentrons P20 8 Channel Electronic Pipette (GEN20)](https://shop.opentrons.com/8-channel-electronic-pipette/)

---

### Deck Setup
* Starting Deck Setup for 2 Reagent Vials:
![deck_setup](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/059126/deck_setup.png)

---

### Protocol Steps
1. Tips are picked up by the P300 starting from the front-right corner of the tip rack. They will be picked up column-wise then row-wise
2. 150 uL is aspirated from the first vial in the 24 well holder A1 and added to each well in the first column
3. Repeat step 2 for each vial specified (up to 12, one for each column)
4. A set amount of each column in the 96 well plate is added with the P20 multichannel to each sample. The net effect is each vial supplied will put a specified amount of its contents in each well.

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
059126

# 357404: Slide sample antibody staining

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample prep
	* Microscopy slide antibody staining

## Description
This protocol performs immunostaining of slides in a custom 3D printed slide block with Shandon coverplates.
Up to 7 slide blocks, each with 8 wells can be placed on the deck resulting in the ability to stain up to 56 slides simultaneously.

Pipette racks and reagents may have to be replaced during the run depending on the number of samples. If that happens the lights of the OT-2 will flash to indicate that the protocol requires the users attention.

Explanation of parameters below:
* `Number of slide blocks`: How many slide holding blocks there are on the deck. The maximum number that will fit on the deck are 7
* `Number of samples in the last block`: All slide blocks except the last one are expected to be full, however the last block may have a number of samples between 1 and 8
* `Volume in reagents containers`: How much volume (µL) there is in each reagent container (meaning block, antibody 1, antibody 2, and nuclear counterstain).
* `Sweep dispense steps`: How many discrete step motions + dispenses to do when dispensing reagents and PBS, this is designed to replicate a sweeping motion with a manual pipette while dispensing. For example if the parameter is set to 5 the pipette will cover the length of the Shandon coverplate mouth in 5 steps and dispense a 5th of the total dispense volume each time.
* `Reagent tuberack`: What type of tuberack you wish to use for the reagents (block, the antibodies and the nuclear counterstain)
* `Pipette offset`: Pipetting offset in `millimeter` when dispensing, increasing this parameter will mean that the pipette will dispense at a lower height in the wells. **This parameter must be adjusted carefully so that there are no collisions between the pipette tip and the Shandon coverplates!**
* `Start protocol after 1st incubation step`: Starts the protocol at the step after the samples have already been incubated with `block`
* `Stop protocol after 1st incubation step`: The protocol stops after adding the block reagent and the user is asked to incubate the samples at 4 degrees C over night.
* `Do a dry run?`: Skip all incubation pauses and return tips to their racks after use.

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Labware
* [Opentrons tuberacks](https://shop.opentrons.com/4-in-1-tube-rack-set/)
* [Agilent 1-Well Reservoir 290 mL](https://labware.opentrons.com/agilent_1_reservoir_290ml)
* [1000 uL tipracks](https://shop.opentrons.com/opentrons-1000-l-tips/)
* [300 uL tipracks](https://shop.opentrons.com/opentrons-300ul-tips-1000-refills/)

### Pipettes
* [P300 single-Channel (GEN2)}](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P1000 single-Channel (GEN2)}](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

### Reagents
290 mL reservoir on slot 2:
* PBS

Reagent tuberack on slot 3:
* Block
* Antibody 1
* Antibody 2
* Nuclear counterstain

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/357404/deck.jpg)

### Reagent Setup
* Reservoir 2: slot 3
![Reagent reservoir](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/357404/reagent_tuberack.jpg)

---

### Protocol Steps
1. The temperature module is set to 4 degrees C.
2. 100 µL of Block is added to the samples wells, unless the protocol is set to skip the 1st reagent addition step.
3. The protocol incubates for 1 hour (with the time it takes to add the Block reagent subtracted)
4. 100 µL Antibody 1 is added (This may be the 1st reagent added in the protocol if the user chooses to start with samples that have been incubated overnight with Block)
5. The protocol incubates for 1 hour
6. The slides are washed with 4 mL Phosphate buffered saline (PBS) each
7. 100 µL of Antibody 2 is added to each slide
8. The protocol incubates for 1 hour
9.  The slides are washed with 4 mL PBS each
10. 100 µL of nuclear counterstain is added to each slide
11. The protocol pauses for 5 minutes
12. The slides are washed with 4 mL PBS each

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
357404

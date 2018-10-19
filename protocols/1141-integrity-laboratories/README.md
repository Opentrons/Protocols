# Mass Spec Sample Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Mass Spec

## Description
This protocol allows your robot to perform mass spec sample prep by letting you select the source container, the number of sources, the destination container, the number of destinations, transfer volume, destination start well, transfer layout strategy, and the single-channel pipette type. Using this protocol, based on the selections you have made, you robot will make multiple identical copies in the destination plates.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".

### Additional Notes
Iteration Strategy:  
![strategy](	https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1141-integrity-laboratories/strategy.png)

Sample number limitation:
Since only 1 sample rack will be loaded in the robot, you need to be mindful when inputing the sample number.
* Opentrons Tuberack 15ml: MAX=12
* Opentrons Tuberack 2ml: MAX=24
* PCR-strip/96 well plate/deep plate: MAX=96

Slot 11 is reserved for your tiprack.

###### Internal
uTU9OHv5
1141

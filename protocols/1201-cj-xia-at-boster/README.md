# ELISA Plate Filling

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to distribute solution from a 1-row trough to 1-9 different 96-well plates, using a 8-channel pipette. The same set of tips are used throughout the entire protocol. User can define which column of tips to use for each run.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input the number of plates (1-9) and the column of tips (1-12) you want to use.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Pipette will pick up the tips from the location you have specified.
8. Using the same set of tips, the pipette will aspirate from the trough and distribute 100 uL of solution into each column of all the plates in the robot.

### Additional Notes
* Make sure the pipette goes to the bottom of the trough when you are calibrating the labware.

###### Internal
pbbWlui3
1201

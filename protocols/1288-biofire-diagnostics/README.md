# Filling Multiple 96 Well Plates

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot will be able to fill 5 96-well plates with a reagent in a 1-well reagent reservoir using 2 P300 multi-channel pipettes. User can define the volume to be transferred into each well.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input your desired volume.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Pipette 1 will aspirate reagent.
8. Pipette 2 will aspirate reagent.
9. Pipette 1 will dispense reagent into column 1 in plate 1.
10. Pipette 2 will dispense reagent into column 2 in plate 1.
11. Robot will repeat steps 7-10 until the desired volume of solution has been transferred. Pipettes will drop tips.
12. Robot will Repeat steps 7-11 until all columns of all 5 plates have been filled.

###### Internal
Ie9C7sRO
1288

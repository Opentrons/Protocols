# 2X Compound Serial Dilution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, your robot will be able to perform 2x serial dilution with from column 11 of the plate down to column 1. The blanks will be in column 12. The robot will dilute 12 samples from your desired container 11 times in a 96-well plate.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Pick your desired container to hold your samples.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will distribute buffer from trough to the entire 96-well plate, 50 uL per well; except for column 11, which will have 90 uL per well.
8. Robot will transfer and mix in 10 uL samples from the first 12 wells of your desired container to each well in column 11 of the 96-well plate.
9. Robot will dilute sample serially down to column 1 by transferring 50 uL solution each time.
10. Robot will discard 50 uL from column 1.

### Additional Notes
Reagent Setup
* Buffer: well A1

Sample Container:
* Make sure there are 12 samples occupying the first 12 wells of the container: A1, B1, C1 ....

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
qrndSVGL
1407

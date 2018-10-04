# FAME's Protocol

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot can transfer 250 uL of two solutions from a 12-column trough to a 96-well plate using a P300 multichannel-pipette, based on your desired number of samples. Number of samples can vary between 1 and 96. The pipette will first pre-wet the tips before aspirating and blow out solutions into the 96 well.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input your desired number of samples.
2. Input the starting column of tips to use.
3. Input the first column in the trough to be drawn from.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will pre-wet the tips by pipetting up and down three times.
10. Robot will transfer 250 uL of first solution to each well.
11. Robot will transfer 250 uL of the second solution to each well

### Additional Notes
If you are using 72 or more samples, and the first column in the trough to be drawn is `2`: fill both A2 and A3 of the trough with the first solution that you would like to transfer, and fill both A4 and A5 of the trough with the second solution. Otherwise, fill only A2 with the first solution and A3 the second.

###### Internal
OCu0HAG5
1280

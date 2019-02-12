# One-Solution FAME's Protocol

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot can transfer 250 uL of solution from a 12-column trough to a 96-well plate using a P300 multichannel-pipette, based on your desired number of samples. Number of samples can vary between 1 and 96. The pipette will first pre-wet the tips before aspirating and blow out solution into the 96 well.

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
10. Robot will transfer 250 uL of solution to each well.

### Additional Notes
If you are using 72 or more samples, fill 2 reservoirs of the trough with the solution that you would like to transfer. If your starting column of trough is `2`, fill both A2 and A3.

###### Internal
Gwj733Yq
1279

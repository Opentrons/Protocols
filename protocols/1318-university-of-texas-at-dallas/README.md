# Serial Dilution for CFU Quantification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Serial Dilution

## Description
With this protocol, your robot can perform serial dilution by transferring PBS from a 12-column trough into a 96-well plate and dilute the solutions down the columns in the plate.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Multichannel pipette will distribute 180 uL PBS from reagent trough to row B to H of the 96-well plate.
7. Single-channel pipette will serial dilute row A down the column by transferring 20 uL. Tip will be changed between each column.

## Additional Notes
* Make sure to remove the A1 tip from the tiprack in **slot 5**. This way the pipette will not distribute PBS to row A in the plate.

###### Internal
qYCAKNii
1318

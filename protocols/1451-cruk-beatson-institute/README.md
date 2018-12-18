# Dilution Series for Biophysical Assays

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, your robot can perform 6 dilutions down a 96-well plate using a P50 and P300 multi-channel pipettes.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer 90 uL buffer from trough to all columns of the 96-well plate.
7. Robot will transfer and mix 10 uL solvent from trough to column 1 of the 96-well plate.
8. Robot will transfer and mix 50 uL of column 1 to column 2.
9. Robot will repeat step 8 until column 6.


### Additional Notes
Trough setup
* Buffer: A1
* Solvent: A2

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
brkM8WuS
1451

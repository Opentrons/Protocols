# Serial Dilutions with Custom 5x12 Rack

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, your robot can perform serial dilutions for up to 36 samples using custom 5 x 12 tube racks. Samples are stored in 10 mL tubes in the 5 x 12 tube rack. Each sample will be diluted 5 times down the rows.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input your desired number of samples.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The robot will transfer 1000 uL diluent from trough to all positions on the dilution racks.
8. The robot will add 50 uL of sample to first row in rack.
9. The robot will perform serial dilutions using 50 uL across 4 rows. Each dilution will be mixed 5 times.

###### Internal
QZA0cDGa
993

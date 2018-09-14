# Minimum Inhibitory Concentrations (MIC) Dilution Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
This protocol allows the robot to prepare serial dilutions (15 dilutions) in 2 columns of a 96-deep well plate and then transfer the solutions to a clean 96-well plate. This protocol requires a P10 multi-channel and P300 multi-channel pipettes.

stock_concentration: float=1600,
initial_concentration: float=16,
dilution_factor: float=2,
dilution_start_column: int=1
### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Set the concentration of your stock solution.
2. Set the concentration of your first dilution.
3. Set your dilution factor.
4. Set the starting column for serial dilution in the 96-deep well plate (max=11).
5. Download your protocol.
6. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".
10. Robot will fill the 2 columns in the 96-deep well plate with buffer from trough.
11. Robot will transfer stock solution from trough to the second well in the second column.
12. Robot will dilute the solution serially by going down the second column, move to the last well of the first column and goes up the column.
13. Robot will transfer the serial dilution to a clean 96-well plate.

### Additional Notes
* Reagent Setup:
    * A1: Stock solution
    * A2: Buffer

###### Internal
hH24r7Gp
1181

# Mass Spec Sample Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocols allows the robot to transfer liquid from four 96-well source plates (slot 1, 2, 3, 4) to individual well of a target 96-well plate (slot 5) using a P10 single-channel pipette.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* DNA buffer

## Process
1. Upload your CSV file following the format below.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Transfer appropriate volume from the appropriate source well to the target well as depicted in the CSV file.

### Additional Information
* Follow this format for the CSV file:

| source plate | source well | source volume | dest plate | dest well |
|--------------|-------------|---------------|------------|-----------|
| 1            | A1          | 5             | 5          | A1        |
| 3            | B7          | 10            | 5          | A2        |
| 2            | C1          | 7             | 5          | D1        |

###### Internal
1tr8KM5J
1115

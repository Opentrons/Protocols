# PCR Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to distribute polymer and PCR reagents from a 12-row trough to a 384-well plate using a single channel pipette. The robot will then transfer the primer stocks from four 96-well plates to the 384-well plate. Volumes of the reagent and primer can be modified in the fields below.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input your desired reagent and primer volumes to be transferred into each well of the 384-well plate.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will distribute the reagent using the P50 single channel pipette. This step is performed without tip change.
8. Robot will transfer the primer from each well in the 96-well plates to each well of the 384-well plate. A new tip is used for each transfer.

### Additional Notes
* When aspirating and dispensing from the well plates, the robot will access each well by going down the columns.  
![well access scheme](	https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1236-environmental-genomics-lab/well_access_scheme.png)

###### Internal
kbgAfa8Q
1236

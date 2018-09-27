# MTT Assay: Part 2/2

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
Part 1 of 2: Drugging

Links: [Part 1](./1155-university-of-toledo_part1) [Part 2](./1155-university-of-toledo_part2)

This protocol allows the robot to perform MTT or similar assays. This protocol has 2 parts: Cell Seeding, and Drugging. During the day of cell seeding, the robot transfers the media and cells in reagent reservoir A1 to all location in a 96-well plate. Each well in a column in the plate will receive identical volume of cell and media. On day 2, the robot performs serial dilution of the drug in a column of a 96-deep well plate specified by the user. The diluted drug solutions are then transferred to the cells.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your volume CSV, input the column of 96-deep well plate for serial dilution as well as the starting tip column for part 2.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
* Volume CSV Format:
    * ![volume csv format](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/MTT_assay/MTT_assay_volume_csv.png)
* Before you start the run, make sure the original stock solution for serial dilution is in the well H of the column you specify in the field above.
* Tiprack setup:
    * Take out the last two tips in the column you specify in the field above, i.e. if you put 2 in Column For Serial Dilution:
    ![tiprack setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/MTT_assay/tiprack.png)

###### Internal
ZWowbj0z
1155

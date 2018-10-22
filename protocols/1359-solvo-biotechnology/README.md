# Serial Dilution and Sample Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, your robot will be able to perform serial dilution by transfer solutions in each row from well 12 trough to 1 in a 96-well plate. After the serial dilutions, the robot will copy the 96-well plate to a 96 deep-well plate. User will be able to specify the column(s) or row(s) that require special mixing steps, the dilution transfer volume as well as the volume to be transferred to the deep well plate.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input the Special Mix Identifiers. See Additional Notes.
2. Input the height for the special mixing steps.
3. Specify the volume to be transferred during serial dilution.
4. Specify the volume to be transferred from the 96-well plate to the deep well plate.
5. Download your protocol.
6. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".
10. Robot will perform serial dilution down each row from well 12 to 1. Tips are changed between each row.
11. Robot will transfer solution from well A1 of the 96 well plate to A1 of the deep well plate.
12. Robot will transfer solution from well B1 of the 96 well plate to B1 of the deep well plate.
13. Robot will repeat 11-12 until all of the wells of the deep well plate have been filled.

### Additional Notes
Serial Dilution Layout:  
![serial dilution layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1359-solvo-biotechnology/serial_dilution_layout_1.png)

Special Mix Identifiers:
* You could put as many identifiers as you would like.
* If you put `1`, only column 1 will be selected: A1, B1, C1 ... H1
* If you put `1, A`, you will be selecting both column 1 and row A: A1, B1, C1 ... H1, and A2, A3, A4, A5 ... A12.
* You can *only* select the entire row and/or column, but not individual well.
* Each identifier needs to be separated by a comma `,`.

Special Mix Height:
* The mixing height for the selected wells defined by an identifier.
* The height is the distance measured from the bottom of the well in mm.

###### Internal
mB7DaY7U
1359

# Transfer Samples from One Plate to Another

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Mapping

## Description
This protocol allows the robot to transfer samples from a source plate to a destination plate using a P10 single-channel pipette. A CSV is required.

Your CSV should look like this:  
![csv format](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1250-stanford-university/csv_format.png)

To generate a `.csv` from Excel or another spreadsheet program, try "File" > "Save As" and select `*.csv`

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your `.csv` in the field above.
2. Select your block A and B container types.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will transfer x uL of sample from plate defined by 'Block Start' to 'Block End'.


### Additional Notes
* Plate A is in slot 1, and plate B slot 2.

###### Internal
fgM6aYRQ
1250

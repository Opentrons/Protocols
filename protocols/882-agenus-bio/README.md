# Transfer samples from 384-well plate to 96-well plate

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Mapping


## Description
Transfers samples from multiple 384-well source plates to multiple 96-well destination plates, using location and volumes input from a CSV file. Protocol uses p300 single-channel and p300 multi-channel pipettes. Protocol begins by distributing 160 uL of media from a trough to all wells of all 96-well destination plates.

To generate a `.csv` from from Excel or another spreadsheet program, try "File > Save As" and select `*.csv`

For example, your CSV could look like this ("portrait" orientation):
![CSV Layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/agenus_bio_csv_layout.png)


Make sure to have the appropriate columns names for your CSV and to have "ul" after your desired volume. Well A1 in each plate is postion 0, well B1 is position 1, C1 is position 2, etc. Position 383 is well P24 for a 384-well plate, and position 95 is well H12 for a 96-well plate. Source and destination plates can use any naming conventions. You can have a maximun of three 384-well source plates.


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input upload your .csv in the field above.
2. Download your protocol.
3. Upload your protocol into the [OT App](http://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your tiprack, pipette, and labware using the OT app. For calibration tips, check out our [support articles](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-pipettes).
6. Hit "run".
7. Robot will transfer 160 uL of media to each well of the 96-well destination plate.
8. Starting with a mixing action to resuspend cells, robot will transfer designated volume of cells from designated well of designated 384-well plate to designated well of designated 96-well plate.
9. Robot will repeat step 9 for each row in the .csv file.

### Additional Notes
Robot will use a new tip for each column of the .csv file. Make sure that there are enough slots on the robot deck for tipracks. For instance, if you have 80 rows in your .csv file, the needs one slot for the tiprack and one slot for the media trough. You have 9 slots remaining for 384-well source plates and 96-well destination plates. However, if you have 100 samples, you need 2 slots for tipracks and one slot for the media trough. You have 8 slots remaining for 384-well source plates and 96-well destination plates.

###### Internal
FFYV8NBK
882

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

```
Source labware label,Source position,Dest labware label,Dest position,Volume
C10-T7 - 03,289,Plate 11,10,160ul
C10-T7 - 03,178,Plate 11,11,160ul
C10-T7 - 03,210,Plate 11,12,160ul
C10-T7 - 03,306,Plate 11,13,160ul
C10-T7 - 03,211,Plate 11,14,160ul
C10-T7 - 03,355,Plate 11,15,160ul
C10-T7 - 03,4,Plate 11,18,160ul
C10-T7 - 03,84,Plate 11,19,160ul
C10-T7 - 03,196,Plate 11,20,160ul
C10-T7 - 03,212,Plate 11,21,160ul
C10-T7 - 03,276,Plate 11,22,160ul
C10-T7 - 03,308,Plate 11,23,160ul
C10-T7 - 03,53,Plate 11,26,160ul
C10-T7 - 03,69,Plate 11,27,160ul
C10-T7 - 03,101,Plate 11,28,160ul
C10-T7 - 03,181,Plate 11,29,160ul
C10-T7 - 03,197,Plate 11,30,160ul
C10-T7 - 03,153,Plate 11,31,160ul
C10-T7 - 03,265,Plate 11,34,160ul
C10-T7 - 03,154,Plate 11,35,160ul
C10-T7 - 03,346,Plate 11,36,160ul
C10-T7 - 03,59,Plate 11,37,160ul
C10-T7 - 03,171,Plate 11,38,160ul
C10-T7 - 03,283,Plate 11,39,160ul
C10-T7 - 02,369,Plate 11,42,160ul
C10-T7 - 02,146,Plate 11,43,160ul
C10-T7 - 02,162,Plate 11,44,160ul
C10-T7 - 02,51,Plate 11,45,160ul
C10-T7 - 02,195,Plate 11,46,160ul
C10-T7 - 02,323,Plate 11,47,160ul
C10-T7 - 02,68,Plate 11,50,160ul
C10-T7 - 02,100,Plate 11,51,160ul
C10-T7 - 02,197,Plate 11,52,160ul
C10-T7 - 02,102,Plate 11,53,160ul
C10-T7 - 02,200,Plate 11,54,160ul
C10-T7 - 02,280,Plate 11,55,160ul
C10-T7 - 02,121,Plate 11,58,160ul
C10-T7 - 02,185,Plate 11,59,160ul
C10-T7 - 02,313,Plate 11,60,160ul
C10-T7 - 02,314,Plate 11,61,160ul
C10-T7 - 02,140,Plate 11,62,160ul
C10-T7 - 02,156,Plate 11,63,160ul
C10-T7 - 02,236,Plate 11,66,160ul
C10-T7 - 02,221,Plate 11,67,160ul
C10-T7 - 02,80,Plate 11,68,160ul
C10-T7 - 01,34,Plate 11,69,160ul
C10-T7 - 01,275,Plate 11,70,160ul
C10-T7 - 01,132,Plate 11,71,160ul
C10-T7 - 01,164,Plate 11,74,160ul
C10-T7 - 01,180,Plate 11,75,160ul
C10-T7 - 01,197,Plate 11,76,160ul
C10-T7 - 01,182,Plate 11,77,160ul
C10-T7 - 01,215,Plate 11,78,160ul
C10-T7 - 01,247,Plate 11,79,160ul
C10-T7 - 01,136,Plate 11,82,160ul
C10-T7 - 01,216,Plate 11,83,160ul
C10-T7 - 01,248,Plate 11,84,160ul
C10-T7 - 01,361,Plate 11,85,160ul
C10-T7 - 01,170,Plate 11,86,160ul
C10-T7 - 01,202,Plate 11,87,160ul
C10-T7 - 01,266,Plate 12,10,160ul
C10-T7 - 01,330,Plate 12,11,160ul
C10-T7 - 01,11,Plate 12,12,160ul
C10-T7 - 01,27,Plate 12,13,160ul
C10-T7 - 01,59,Plate 12,14,160ul
C10-T7 - 01,75,Plate 12,15,160ul
C10-T7 - 01,171,Plate 12,18,160ul
C10-T7 - 01,203,Plate 12,19,160ul
C10-T7 - 01,44,Plate 12,20,160ul
C10-T7 - 01,76,Plate 12,21,160ul
C10-T7 - 01,236,Plate 12,22,160ul
C10-T7 - 01,332,Plate 12,23,160ul
C10-T7 - 01,61,Plate 12,26,160ul
C10-T7 - 01,158,Plate 12,27,160ul
C10-T7 - 01,318,Plate 12,28,160ul
C10-T7 - 01,334,Plate 12,29,160ul
C10-T7 - 01,366,Plate 12,30,160ul
C10-T7 - 01,382,Plate 12,31,160ul
C10-T7 - 01,63,Plate 12,34,160ul
C10-T7 - 01,79,Plate 12,35,160ul
C10-T7 - 01,111,Plate 12,36,160ul
C10-T7 - 01,383,Plate 12,37,160ul
```

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

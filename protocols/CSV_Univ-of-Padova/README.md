# Library Concentration Normalization

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Chemistry
	* Dilution

## Description
Normalization of library concentrations using volume and location inputs from a CSV. Uses a p50, p300, or p1000 single channel pipette (changed in the customization field in the Python script). Transfer designated volumes of solvent from a 15 mL tube to a designated well in a 96-well putput plate. Mixing after each solvent transfer is optional.

To generate a `.csv` from from Excel or another spreadsheet program, try "File > Save As" and select `*.csv`

Your CSV should look similar to this:

```
#COMMENT LINE,,
# CMPD-ID,PLATE-POSITION,volume_to_be_added_to_the_weel (uL)
1000,A5,25
1001,A6,32
1004,B4,43
```

There can be 1-96 row entries in this list because you only have 96 pipette tips available. You use a new tip for each well of the normalization process.

### Time Estimate

### Robot
* OT-2

### Modules

### Reagents
* Solvent (e.g. DSMO)

## Process
1. Input your CSV file in the field above.
2. Download your protocol.
3. Upload your protocol into the OT App.
4. Set up your deck according to the deck map.
5. Calibrate your tiprack, pipette, and labware using the OT app.
6. Hit "run".

Protocol begins:

7. The robot will aspirate the volume designated in row one, column 3 of the CSV from 'A1' in a 15-50 tuberack.
8. The robot will dispense that volume in the well of the output 96-well plate designated by row one, column 2 of the CSV.
9. The robot repeats this for all the entries in the CSV file.

### Additional Notes
Make sure not to change the labels of each column in the CSV. If you do, adjust the .py (Python) script accordingly. Make to adjust max volume customization field to use appropriate single channel pipette.

###### Internal
dVgtln5g
1015
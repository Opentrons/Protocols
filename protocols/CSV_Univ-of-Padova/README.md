# Library Concentration Normalization

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Chemistry
	* Dilution

## Description
Normalization of library concentrations using volume and location inputs from a CSV. Uses a p50, p300, or p1000 single channel pipette (changed in the customization field in the Python script). Transfer designated volumes of solvent from a 15 mL tube to a designated well in a 96-well output plate. Mixing after each solvent transfer is optional.

To generate a `.csv` from from Excel or another spreadsheet program, try "File > Save As" and select `*.csv`

Your CSV should look similar to this:  

![csv layout](	https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/CSV_Univ-of-Padova/csv_layout.png)

There can be 1-96 row entries in this list because you only have 96 pipette tips available. You use a new tip for each well of the normalization process.

### Robot
* OT-2


### Reagents
* Solvent (e.g. DSMO)

## Process
1. Input your CSV file in the field above.
2. Select whether or not you would like the pipette the mix the liquid after each transfer.
3. Download your protocol.
4. Upload your protocol into the OT App.
5. Set up your deck according to the deck map.
6. Calibrate your tiprack, pipette, and labware using the OT app.
7. Hit "run".

Protocol begins:

8. The robot will aspirate the volume designated in row one, column 3 of the CSV from 'A1' in a 15-50 tuberack.
9. The robot will dispense that volume in the well of the output 96-well plate designated by row one, column 2 of the CSV.
10. The robot repeats this for all the entries in the CSV file.

### Additional Notes
* Make sure to keep the same layout of the CSV as shown above. The first two line of the CSV will be ignored. Therefore, make sure your list of wells starts from column 2 line 3, and list of volumes starts from column 3 line 3.

###### Internal
dVgtln5g
1015

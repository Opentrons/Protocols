# Sample Serial Dilution and Cell Culture Addition

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Distribution

## Description
Uses p300 multi channel pipette on left mount. Water and cells in various wells of a 12-row trough (locations within trough customizable). With sample preloaded into column 1 of a 96-well flat plate, robot transfer 100 uL sterile water into the plate (right to left to avoid sample carry-over). Sample is serially dilutes across the plate based on customizable dilution factor. Last column excess volume is disposed of in trash bin so all columns have same total volume. Robot adds 100 uL on cells to all wells of 96-well flat plate, getting new tips for each column.

### Time Estimate

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* Sterile water
* Sample

## Process
1. Set well location of sterile water and cells in 12-row trough in slot 2.
2. Set dilution factor of sample across plate where dilution factor = (water volume + sample volume) / sample volume.
3. Download protocol, and upload into the app.
4. Robot will transfer 100 uL of sterile water from the trough into each column of 96-well plate, starting at column 12 and ending with column 1.
5. Robot will get fresh tips and transfer a volume of sample from column 1 into column 2 (transfer volume determined by dilution factor).
6. Robot will mix column 2 three times at half the total volume of contents in column 2.
7. Robot will repeat steps 5-6 for columns 1-12, getting fresh tips for every transfer.
8. Robot will transfer the excess volume in column 12 to the trash bin to keep total volume of all columns in 96-well plate constant.
9. Robot will add 100 uL of cells from the trough to all wells of the 96-well plate, getting fresh tips between tranfers.


### Additional Notes
Dilution Factor = (Water Volume + Sample Volume) / Sample volume

Water volume is fixed at 100 uL. Dilution factor is set by user. Sample volume volume transfer across the plate is calculated in protocol.

###### Internal
iJkPh9XP
1328

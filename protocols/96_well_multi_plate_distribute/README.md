# Fill several 96 well plates from 1x 96 well plate

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Basic Pipetting
	* Plate Filling


## Description
Distribute contents of a 96-well source plate to up to 13* empty 96-well destination plates, using an 8-channel pipette. Row 1 of the source plate will  go to Row 1 of all destination plates, and so on for all 12 rows of the plate.

**Note:** the OT Hood model will only accommodate up to 8 empty plates, not 13.

Add destination plates to robot slots in this order: A1, B1, C1, D1, A2, B2, D2, E2, A3, B3, C3, D3, E3.
	* For example, with 3 destination plates, use slots A1, B1, and C1



### Time Estimate
Varies

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](https://opentrons.com/ot-one-hood)

### Modules

### Reagents

## Process
1. Load a 96-well source plate, containing liquid to be distributed, to slot C2.
2. Robot transfers Row 1 from the source plate to Row 1 of all destination plates.
3. Step 2 is repeated for all 12 rows of the source plate.


### Additional Notes

###### Internal
149

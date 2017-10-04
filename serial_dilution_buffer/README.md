# Customizable Serial Dilution

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Basic Pipetting
	* Dilution


## Description
Customizable serial dilution. Performed across 1 to 6 96-well plates.

The plates should already be loaded up manually with samples, across row 1 of the plate.

For the 96-well plates, place into slots on the robot in this order: A1, B1, A2, B2, A3, B3.
* (Ie for 3 plates, use A1, B1, A2.)

For the tipracks, fill the slots on the robot in this order: C1, C3, D1, D3, E1, E2, E3.

### Time Estimate
Varies

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](https://opentrons.com/ot-one-hood)

### Modules

### Reagents

## Process
1. Off-robot: operator manually adds samples to Column 1 of each plate
2. For first plate: fill rows with uniform volume of diluent. Only as many rows specified in "Number of Rows to Use" will be used.
3. Dilute up across the rows of the plate according to the specified Dilution Factor
4. Discard the excess volume in the last row into the trash
5. Repeat steps 2-4 for the each of the remaining plates


### Additional Notes


###### Internal
nszsx2Zy
250

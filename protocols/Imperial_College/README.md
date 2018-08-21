# Drug Mixing and Transferring

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Consolidation


## Description
This protocol allows you to add different combination of compounds from several 96-well plate to each well of a 24-well plate for mixing using a single-channel pipette. Each of these 24 wells will then be transferred to a clean 24-well plate. The compound source information and target locations are defined in a CSV file.

### Time Estimate

### Robot
* [OT 2](https://opentrons.com/ot-2)
* [OT PRO](https://opentrons.com/robots/ot-one-s-pro)
* [OT Standard](https://opentrons.com/robots/ot-one-s-standard)  

## Process
1. Upload a CSV file containing information of compound source and target.
2. Download the protocol for the appropriate robot.


### Additional Notes
CSV files breakdown:
* Compound: name of compound
* Plate: the plate in which the compound is stored
* Well: the well of the plate in which the compound is stored
* A1, B1 ,,,, D6: volume of which the compound is to be transferred to each individual target well A1, B1 ,,,, D6

![CSV Example](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/volume_csv_example.png)

###### Internal
fBpgkSb3
1034

# ELISA Preparation with Dilutions in Deepwell Plate

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Immunoresearch Lab](https://www.jacksonimmuno.com/)

## Categories
* Proteins & Proteomics
	* Assay


## Description
Preparation of two samples for an ELISA assay. Uses p1000 and p300 single channel pipettes. Samples are in 2-mL tubes in 2mL tuberack (wells A1 and B1). 1:100 and 1:2500 dilution of samples are made of each sample in 2mL tubes at locations A2/B2 and A3/B3, respectively. Buffer for dilutions is in row 1 of a 12-row trough. Dilutions are made in a 96-well deepwell plate before transfering in duplicate to a regular 96-well output plate.

### Time Estimate

### Robot
* OT-2

### Modules

### Reagents
* Buffer for dilution 

## Process
Add buffer to all appropriate locations:

1. Transfer 495 uL buffer to well A2 of 2mL rack.
2. Transfer 960 uL buffer to well B2 of 2mL rack.
3. Transfer 495 uL buffer to well A3 of 2mL rack.
4. Transfer 960 uL buffer to well B3 of 2mL rack.
5. Transfer 1080 uL buffer to column 1, row A/E/C/G of deepwell plate.
6. Transfer 800 uL buffer to columns 2-11, row A/E/C/G of deepwell plate.
7. Transfer 200 uL buffer to column 12, row A/E/C/G of output 96-well plate.

Add samples to buffer and transfer dilutions to output 96-well plate:

8. Transfer 5 uL of sample to well A2. Mix 5 times at 50 uL.
9. Transfer 40 uL from well A2 to well A3. Mix 5 times at 50 uL.
10. Transfer 120 uL from well A3 to deepwell well A1. Mix 5 times at 500 uL.
11. Transfer 200 uL from deepwell A1 to output plate A1 and B1. 
12. Repeat steps 8-11 for sample 2 in appropate wells.
13. Transfer 120 uL from well A2 to deepwell C1. Mix 5 times at 500 uL.
14. Transfer 200 uL from deepwell C1 to output plate C1 and D1. 
15. Repeat steps 13-14 for sample 2 in appropriate wells.

Complete sample dilutions across deepwell plate and transfer to output plate:

16. Transfer 400 uL from deepwell A1 to deepwell A2. Mix 5 times at 500 uL.
17. Transfer 200 uL from deepwell A2 to output plate A2 and B2. 
18. Repeat step 16-17 until for columns 2-11 of row A.
19. Repeat step 18 for rows C, D, and G of deepwell plate. 

### Additional Notes

###### Internal
pLhC4ZG9
1089
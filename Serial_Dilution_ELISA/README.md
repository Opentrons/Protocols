# ELISA

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins and Proteomics

## Description
* Prepare the ELISA plate by pre-washing with EGRF and let the solution sit
for 16 hours. Then wash the plate with wash buffer 4x and superblock.
* Prepare the samples through a simple 5-fold serial dilution with a ending
concentration of 1000 ng/ml - this program calculates that for you.
You may either manually input stock solutions or input a CSV file.
* Place the diluted samples in the ELISA reaction plate.
* Wash plate again with wash buffer 4x.
* Put in secondary antibody.
* Stop reaction with TMB and sulfuric acid.

### Time Estimate
16 hours and 45 minutes

### Robot
* OT PRO
* OT Standard
* OT Hood

## Process
1. Place plates, tip-racks and troughs in their designated locations.
2. Open the OT app found on Opentrons website and upload the .py file.
3. Calibrate each container used in the protocol.
4. Hit run and let the robot do the rest!

###### Internal
Protocol written for R-Pharm.

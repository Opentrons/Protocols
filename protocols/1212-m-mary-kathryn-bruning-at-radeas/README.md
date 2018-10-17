# Procedure for QC 50mL Pipette

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
This protocol requires two custom containers, a 5x10 vial tray and a 8x12 cuvette tray.


## Process
1. Choose the volumes for each step as follows:
QC_Conc1000, default is 100.0, transferring QC to cuvette tray location C1
BuffA_Conc1000, default is 100.0, transferring BuffA to cuvette tray location C1
urine_Conc1000, default is 100.0, transferring urine to cuvette tray location C1
urine_Conc200, default is 800.0, transferring urine to cuvette tray location C2
urine_Conc20, default is 800.0, transferring urine to cuvette tray location C3
dilute_Conc200by1000, default is 200.0, transferring from C1 -> C2
dilute_Conc20by200, default is 100.0, transferring from C2 -> C3
QC_highvol, default is 800.0, transferring from cuvette A5 -> glass vial A1/A2
QC_lowvol, default is 800.0, transferring from cuvette A6 -> glass vial C1/C2
std3_vol, default is 50.0, transferring from A7 -> glassvial A1-C2
add_Conc200, default is 400.0, transferring from cuvette C2 -> glass vial A1/A2
add_Conc20, default is 400.0, transferring from cuvette C3 -> glass vial C1/C2

###### Internal
Z2prAvc2
1212

### Additional Notes

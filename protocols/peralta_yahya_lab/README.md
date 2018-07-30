# Flow Cytometry Preparation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Distribution

## Description
This protocols allows the robot to perform flow cytometry preparation by transferring media, chemical, and cells into wells B2-G11 of up to 4 different plates.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* Yeast media
* Chemicals in DMSO
* Yeast cells

## Process
1. Download your protocol.
2. Upload your protocol into [OT App](https://opentrson.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your tiprack, pipette, and labware using the OT app. For calibration tips, check out our [support articles](https://support.opentrons.com/getting-started/software-setup/calibrating-the-pipettes).
5. Hit "run" and watch your robot do the rest!
6. Fills the wells B2-G11 of the target 96-well plates (P2, P4, P5, and P6) with 182 uL of media from a 50 mL tube using a P300_Single pipette.
7. Aspirates 30 uL of chemical from P1 wells A1-F1 and dispenses into B2-G2, B5-G5, B6-G6 of P2 using a P50_multi pipette.
8. Aspirates 30 uL of chemical from P1 wells A2-F2 and dispenses into B3-G3, B6-G6, B9-G9 of P2.
9. Aspirates 30 uL of chemical from P1 wells A3-F3 and dispenses into B4-G4, B7-G7, B10-G10 of P2.
10. Repeat the pattern of steps 2-4 three more times to finish filling P4, P5, and P6 with chemicals on the rest of the P1 columns (A4-A12).
11. Transfers 8 uL of cells from P3 wells B2-G2 to wells B2-G11 of all the target wells plates. Tips are changed every time the pipette goes back P3.

### Additional Notes
Tips need to be manually removed from wells G1-H12 of tiprack in slot 7 to prevent pipette from hindering the liquid transfer.

###### Internal
5RSj7YYX
904

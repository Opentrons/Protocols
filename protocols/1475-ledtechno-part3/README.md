# ELISA Assay 3/5: Addition of Samples

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
Links:
* [Part 1: Plate Coating](./1475-ledtechno-part1)
* [Part 2: Addition of Blocking Buffer](./1475-ledtechno-part2)
* [Part 3: Addition of Samples](./1475-ledtechno-part3)
* [Part 4: Addition of Detection Antibody](./1475-ledtechno-part4)
* [Part 4: Addition of Avidin-HRP, TMB Substrate, Stop Solution](./1475-ledtechno-part5)

Day 2: The plate is washed 3 times with 300 uL wash buffer 100 uL of standard samples and test samples are added to the plate.

---

You will need:
* P300 Multi-channel Pipette
* P100 Single-channel Pipette
* 96-well Plate
* 24-well Plates
* 12-row Trough

### Robot
* [OT-One](https://opentrons.com/robots)

## Process
1. Download your protocol.
3. Upload your protocol onto the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your tiprack, pipette, plate, and petri dishes using the OT App. For calibration tips, check out our support articles:
 * [Calibrating the Deck](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-deck)
 * [Calibrating the Pipettes](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-pipettes)
6. Hit "Run Job".
7. Robot will transfer 300 uL wash buffer to the whole plate.
8. Robot will discard solutions in each well.
9. Robot will repeat steps 7-8 twice.
10. Robot will pause for 2 minutes for user to remove all residual buffer by tapping the plate upside down on absorbent paper.
11. Robot will transfer 18 standard samples from 24-well standard plates to 96-well plate.
12. Robot will transfer 78 test samples from 24-well sample plates to 96-well plate.

### Additional Notes
Trough:
* Wash Buffer: A1-A4

Standard Samples (18 wells):
* A1-B5

Test Samples (78 wells):
* Sample Plate (slot A2): A1-D6
* Sample Plate (slot A3): A1-D6
* Sample Plate (slot B2): A1-D6
* Sample Plate (slot B3): A1-B2

###### Internal
7RuzcYGS
1475

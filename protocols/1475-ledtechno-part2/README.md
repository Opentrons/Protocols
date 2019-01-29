# ELISA Assay 2/5: Addition of Blocking Buffer

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

Day 2: The plate is washed 3 times with 300 uL wash buffer and 200 uL blocking buffer is to be added to each well.

---

You will need:
* P300 Multi-channel Pipette
* 96-well Plate
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
11. Robot will transfer 200 uL blocking buffer to each well.

### Additional Notes
Trough:
* Wash Buffer: A1-A4
* Blocking Buffer: A7

###### Internal
7RuzcYGS
1475

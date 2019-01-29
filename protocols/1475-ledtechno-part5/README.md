# ELISA Assay 5/5: Addition of Avidin-HRP, TMB Substrate, Stop Solution

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

Day 2: The plate is washed 3 times with 300 uL wash buffer and 100 uL Avidin-HRP antibody is to be added to each well. After a pause, robot will wash the plate 4 times with 300 uL wash buffer, and add 100 uL TMB substrate to each well. After another pause, robot will finally add 100 uL stop solution to each well to complete the protocol.

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
10. Robot will pause for user to remove all residual buffer by tapping the plate upside down on absorbent paper.
11. Robot will transfer 100 uL Avidin-HRP to each well.
12. Robot will pause for user to incubate the plate with shaking. User should refill the wash buffer and empty the liquid trash before resuming the protocol.
13. Robot will wash the plate 4 times with wash buffer, robot will pause for user to remove residual buffer.
14. Robot will add 100 uL TMB substrate to each well.
15. Robot will pause for user to incubate plate without light.
16. Robot will add 100 uL stop solution to each well.

### Additional Notes
Trough:
* Wash Buffer: A1-A4
* Avidin-HRP: A9
* TMB substrate: A10
* Stop solution: A11

###### Internal
7RuzcYGS
1475

# Drug Screening

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
Using this protocol, your robot can perform drug screening on a 96-well plates using 4 different drugs. Drug A will be distributed to column 1-3, drug B to column 4-6, drug C to column 7-9, and drug D to column 10-12. After 30 minutes of incubation, the robot will remove the drugs from the wells and distribute Drug E to all the wells.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will consolidate and discard solution from column 1-3, then use a new set of tips to distribute drug A to the columns.
7. Robot will consolidate and discard solution from column 4-6, then use a new set of tips to distribute drug B to the columns.
8. Robot will repeat steps 6-7 for the rest of the plate, using drug C and D.
9. Robot will pause for 30 minutes for incubation.
10. Robot will remove drug from column 1-3, then distribute drug E.
11. Robot will remove drug from column 4-6, then distribute drug E.
12. Robot will repeat steps 10-11 until the entire plate is filled with drug E.

### Additional Notes
Trough setup
* Drug A: well A1
* Drug B: well A2
* Drug C: well A3
* Drug D: well A4
* Drug E: well A5

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
noms9Vbw
1430

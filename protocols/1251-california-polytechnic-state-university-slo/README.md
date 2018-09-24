# Cell-Free Protein Synthesis Reaction Setup

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot can generate cell-free protein synthesis reaction setup using information uploaded in a CSV. The CSV contains volumes of each reagent that should be dispensed into the each of destination well. Please see format of the CSV in Additional Notes.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* Water: well A1
* Extract: well B1
* DNA: well C1
* Buffer 1 (A-E): well D1-D2
* Buffer 2 (A-E): well A3-A4
* Buffer 3 (A-E): well B4-B5
* Solution A: well C5
* Solution B: well D5

## Process
1. Upload your volume CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will distribute water to each well.
8. Robot will mix extract 5 times, then distribute extract to each well. Extract will be mixed twice before each aspiration.
9. Robot will mix DNA 5 times, then distribute extract to each well. DNA will be mixed twice before each aspiration.
10. The robot will distribute each buffer from group 1 to the appropriate well.
11. The robot will distribute each buffer from group 2 to the appropriate well.
12. The robot will distribute each buffer from group 3 to the appropriate well.
13. The robot will mix solution A 10 times, then distribute to groups of 8 wells. A new tip will be used and solution will be mixed 5 times before each aspiration.
14. The robot will mix solution B 15 times, then distribute to groups of 8 wells. A new tip will be used and solution will be mixed 10 times before each aspiration.
15. The robot will mix each PCR tube twice. A new tip will be used for every 4 tubes.

### Additional Notes
* Make sure to follow this CSV Format:

![csv_format](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1251-california-polytechnic-state-university-slo/csv_format.png)


###### Internal
PgcWOxvq
1251

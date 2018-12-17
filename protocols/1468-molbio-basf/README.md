# Serial Dilution of Inhibitor in Media

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, your robot can perform serial dilution of inhibitor in a 96-deep well plate.

---

You will need:
* P50 Multi-channel Pipette
* P300 Single-channel Pipette
* [12-row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* 96-Deep Well plate
* [Opentrons 300 uL Tip Racks](https://shop.opentrons.com/collections/opentrons-tips)

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
6. Robot will transfer 250 uL solution 1 to all wells of the deep well plate.
7. Robot will transfer and mix 250 uL solution 2 to well A1, and perform serial dilution down column 1 until well G1.
8. Robot will discard 250 uL from G1.
9. Robot will repeat step 7-8 for all 12 columns.
10. Robot will transfer sample 1 to column 1, 2, and 3 of deep well plate.
11. Robot will transfer sample 2 to column 4, 5, and 6 of deep well plate.
12. Robot will transfer sample 3 to column 7, 8, and 9 of deep well plate.
13. Robot will transfer sample 4 to column 10, 11, and 12 of deep well plate.

### Additional Notes
Trough Setup
* Solution 1: A1
* Solution 2: A2
* Sample 1: A3
* Sample 2: A4
* Sample 3: A5
* Sample 4: A6

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
51dL0W7T
1468

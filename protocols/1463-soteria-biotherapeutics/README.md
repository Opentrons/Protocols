# Cell Culture Assay with Drugs, Growth Media and Stimulation Media

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Cell Feeding

## Description
With this protocol, your robot will transfer diluted drugs to cell culture in a 96-well plate.

---

You will need:
* P50 Single-channel Pipette
* P300 Multi-channel Pipette
* 96-deep Well Plate
* [96-well U-bottom Plate](https://www.fishersci.com/shop/products/falcon-tissue-culture-plates-96-well-non-treated-u-bottom-growth-area-0-36cm2-well-volume-0-32ml-1-tray/0877254)
* 12-well Trough
* 200 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer 900 uL growth media to column 1-10 of the Drug Dilution Plate in slot 4.
7. Robot will transfer and mix 50 uL Drug A in well A11 to well A10.
8. Robot will transfer and mix 50 uL Drug B in well A12 to well A10.
9. Robot will serially dilute from well A10 to A2 with 100 uL.
10. Robot will repeat step 7-9 for row B and C.
11. Robot will mix and transfer 33 uL cells to column 2-11 of the Assay Plate in slot 1.
12. Robot will transfer 33 uL diluted drugs from column 1-10 of the Drug Dilution Plate to column 2-11 of the Assay Plate.
13. Robot will pause for user to transfer the plate to an incubator.
14. Robot will transfer 33 uL stimulation media to column 2-11 of the Assay Plate.


### Additional Notes
Trough Setup:
* Cells: A1
* Growth Media: A2
* Stimulation Media: A3

---

Drug Setup:
* Drug A: wells A11, B11, C11
* Drug B: wells A12, B12, C12

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
J61sGBFZ
1463

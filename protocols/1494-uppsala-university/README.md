# Cell Painting

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Cell Painting

## Description
With this protocol, you can perform cell painting using MitoTracker, 4% PFA, 0.1% Triton, and Staining Solution on 60 samples (well B2-G11) in a 96-well plate. Reagent and plate layout can be found in Additional Notes.

---

You will need:
* P300 Multi-channel Pipette
* [Agilent Single-cavity Reservoirs](http://agilentmicroplates.com/products/201244-100/)
* [Agilent 4-column Reservoirs](http://agilentmicroplates.com/products/201308-100/)
* Tiprack

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
6. Robot will mix Mitotracker, remove plate contents (70 uL/well), distribute 30 uL Mitotracker to each well.
7. Robot will pause until user to resume the protocol.
8. Robot will remove plate contents (30 uL/well), wash plate twice with 60 uL PBS1, add 50 uL 4% PFA.
9. Robot will remove plate contents (50 uL/well), wash plate twice with 60 uL PBS2.
10. Robot will mix and add 50 uL 0.1% Triton and pause and let plate incubate for 20 minutes.
11. Robot will remove plate contents (50 uL/well), wash plate twice with 60 uL PBS1.
12. Robot will mix and add 50 uL staining solution to each well.
13. Robot will pause until user resume the protocol.
14. Robot will remove plate contents (50 uL/well), wash plate twice with 60 uL PBS3.
15. Robot will distribute 90 uL PBS3 to each well.


### Additional Notes
Deck Layout:

![deck_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1494-uppsala-university/deck_layout.png)

---

Tip Rack:
* Make sure you remove row A and row H of the tip rack

---

Trough 4-column:
* Mitotracker: Well A1
* 4% PFA: Well A2
* 0.1% Triton: Well A3
* Staining Solution: Well A4

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal

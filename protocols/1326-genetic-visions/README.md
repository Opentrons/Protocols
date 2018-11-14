# Nucleic Acid Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Purification

## Description
This protocol allows your robot perform nucleic acid purification using reagents from a trough filled with 4 [Beckman Coulter Modular Reservoir Quarter Modules](https://www.beckman.com/supplies/reservoirs/372788). This protocol requires a P300 multi-channel pipette.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will distribute 65 uL of reagent from well A1 of the reservoir to all columns of a 96-well plate in slot 1.
7. Robot will distribute 200 uL of reagent from well A2 of the reservoir to all columns of a 96 deep-well plate in slot 2.
8. Robot will distribute 500 uL of reagent from well A1, A2, and A3 of the reservoir in slot 8 to all columns of a 96 deep-well plate in slot 3 and slot 6.

### Additional Notes
Deck Layout:
* Elution Plate: slot 1
* EtOH Plate: slot 2
* Buffer 1 Plate: slot 3
* Buffer 2 Plate: slot 6
* 4-column Trough: slot 5
* 4-column Trough: slot 8

Reagent Setup:
* Tris HCl: slot 5 well A1
* EtOH: slot 5 well A2
* Wash Buffer: slot 6 wells A1, A2, A3


###### Internal
uq81xsju
1326

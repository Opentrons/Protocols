# PCR/qPCR Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR

## Description
To begin the protocol, your robot will distribute water to a clean 96-well plate. The robot will then create your primer mixture in a 96-well plate by copying 2 primer plates into the plate. The mixture and DNA will be transferred into a new plate. Lastly, the mastermix will be distributed into this plate.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer 180 uL of water from trough A1 to all wells in a new 96-well plate (Plate X) using the P300 multi-channel pipette.
7. Robot will transfer 10 uL of primer 1 from its original 96-well plate (Plate P1) to all wells in Plate X using the P50 multi-channel pipette.
8. Robot will transfer and mix 10 uL of primer 2 from its original 96-well plate (Plate P2) to all wells in Plate X using the P50 multi-channel pipette.
9. Robot will transfer 2 uL of primer mixture to all wells in a new 96-well Plate Y using the P10 multi-channel pipette.
10. Robot will transfer 3 uL of DNA from its original 96-well plate (Plate DNA) to all wells in Plate Y using the P10 multi-channel pipette.
11. Robot will transfer 23 uL of master mix from trough well A2 to all wells in Plate Y using the P50 multi-channel pipette.

### Additional Notes
Deck Setup:
* Plate DNA: slot 1
* Plate Y: slot 2
* Plate X: slot 3
* Trough: slot 4
* Plate 1: slot 5
* Plate 2: slot 6

** Note: water is in well A1 of trough, and master mix A2

###### Internal
ryI0DStE
1352

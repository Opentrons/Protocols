# Liquid Transfer from 96-Well Plates to a 384 Well Plate

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to transfer DNA from four 96-well plates to a single 384-well plate using a multi-channel pipette (P50 or P300). Transfer volume is customizable. See Additional Notes for robot deck layout.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input your desired volume to be transferred into each well of the 384-well plate.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer plate 1 to A1, C1, E1..., A3, C3, E3....., A23, C23, E23...
8. Robot will transfer plate 2 to A2, C2, E2..., A4, C4, E4....., A24, C24, E24...
9. Robot will transfer plate 3 to B1, D1, F1..., B3, D3, F3....., B23, D23, F23...
10. Robot will transfer plate 4 to B2, D2, F2..., B4, D4, F4....., B24, D24, F24...

### Additional Notes
* Plate 1: slot 1
* Plate 2: slot 2
* Plate 3: slot 4
* plate 4: slot 5

###### Internal
EgLdA62Y
1222

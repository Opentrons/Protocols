# 384-Well Plate Mapping

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot can perform plate mapping of a 384-well source plate to up to 6 384-well destination plates using a P10 multi-channel pipette. You can specify the volume to be transferred into each destination well.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input the number of destination plates. (Max = 6)
2. Input the volume to be transferred to each destination well.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will distribute wells from rows A, C, E, G, I, K from the first column of source plate to that of all destination plates.
9. Robot will distribute wells from rows B, D, F, H, J, L from the first column of source plate to that of all destination plates.
10. Repeat steps 8 and 9 until all columns of the source plate has been distributed.

###### Internal
0wCvbVlp
1310

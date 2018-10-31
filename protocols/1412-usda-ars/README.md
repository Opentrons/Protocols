# Plate Mapping and Dye Distribution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Mapping

## Description
Robot can perform basic plate mapping from a 96-well plate to another, as well as liquid distribution to the second plate from a 12-row trough. In this protocol, the robot will use a P10 multi-channel pipette to copy PCR products from one plate to the other using the same tips. Tips will be rinsed by pipetting up and down in the water reservoir between each sample transfer. User can define the volume of PCR product and dye to be transferred to the second 96-well plate. Refer to Process and Additional Notes for more information on this protocol.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input your desired PCR volume to be transferred to the second 96-well plate.
2. Input your desired loading dye volume to be transferred.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will transfer samples from the sample plate in slot 1 to the output plate in slot 2 column-by-column.
9. Robot will rinse the same tips with water between each column.
10. Robot will repeat steps 8-9 until all of the columns in the sample plate have been transferred.
11. Robot will use a new set of tips to transfer the loading dye to each column of the output plate.

### Additional Notes
Deck Layout:
* Input Plate: Slot 1
* Output Plate: Slot 2
* Trough: Slot 3
* Tip Rack: Slot 5

Trough Setup:
* Water: Well A1
* Loading Dye: Well A2

###### Internal
G3AtrWBe
1412

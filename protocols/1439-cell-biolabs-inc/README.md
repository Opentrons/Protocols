# ELISA Plate Washing

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot can perform ELISA plate washing on up to four 96-well plate by (1) distributing plate washing solution to each well of the plates, and (2) aspirating all of the washing solution from each individual well and discard in waste container.

---

You will need:
* P300 Multi-channel Pipette
* 96-well Plate
* [1-chamber Trough](http://www.eandkscientific.com/8-Row-Reservoir-Deep-Well-Undivided-Pyramid-Bottom-290ml.html)
* [Opentrons 300 uL Tip Racks](https://shop.opentrons.com/collections/opentrons-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input the number of plate you will be processing.
2. Input the volume of plate washing solution to be transferred to each plate.
3. Select your tip change strategy for removing washing solution: `use one set of tips only` uses the same tips to aspirate from each well, `new tip each well` uses a new tip for each transfer.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will transfer plate washing solution from trough to plates.
10. Robot will remove plate washing solution from plates to an empty trough.

### Additional Notes
Trough Setup
* Plate Washing Solution: slot 1
* Liquid Trash: slot 4

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ycNNg6q2
1439

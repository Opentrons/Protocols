# RBC Transfer

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Blood Sample

## Description
With this protocol, your robot can perform blood samples from blood tubes to each well of a 96-well plate. After the transfer, BF3 and WISTD are then added to each sample in the 96-well plate.

---

You will need:
* P50 Single-channel Pipette
* P300 Multi-channel Pipette
* Glass Troughs
* 96-well Plate
* Opentrons 300 uL Tip Rack
* Extended 200 uL Tip Rack


### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Set the number of samples you will be processing in this run.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 25 uL blood samples from blood tube to 96-well plate. Robot pauses for 3 seconds after drawing the blood to ensure sample is properly aspirated.
8. Robot will distribute 250 uL BF3 from glass trough to each sample in the plate.
9. Robot will distribute 250 uL WISTD from glass trough to each sample in the plate.

### Additional Notes
Reagent Layout:
* BF3: slot 3
* WISTD: slot 5

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
p1Xtre5x
1498

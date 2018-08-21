# PCR/qPCR Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to perform PCR, qPCR prep or any similar assays. This requires two CSV inputs, one is the volumes of samples, the other is the volume of MilliQ water to be dispensed into each individual well of a 96-well plate.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your CSVs in the fields above.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Dispense appropriate volume of each sample from a 96-well plate to the appropriate well of 96-well dilution plate.
8. Dispense appropriate volume of MilliQ water from a trough to the appropriate well of 96-well dilution plate.
9. Transfer 2 uL from dilution plate to a new PCR plate.
10. Transfer 23 uL PCR mix into each well of PCR plate.

###### Internal
RhEypQsk
994

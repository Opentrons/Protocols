# Pooling 96 Samples to a Single 1.5 / 15 mL

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Consolidation

## Description
With this protocol, your robot can consolidate all samples in a 96-well plate into a single tube, either 1.5 mL or 15 mL. User can specify the volume to pick from the wells, as well as the destination tube.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Input the volume to be transferred from each sample into the tube.
2. Select the tube rack type.
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer sample in plate well A1 to tube rack well A1.
7. Robot will transfer sample in plate well B1 to tube rack well A1.
8. Robot will transfer samples from the rest of the plate into tube rack well A1.

### Additional Note
Setup
* Sample Plate: Slot 1
* 15 mL/2 mL Tube Rack: Slot 2

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
qNSHMgnB
1223

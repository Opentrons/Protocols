# RNA Quantification: 96 Samples

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Mapping

## Description
This protocol allows your robot to (1) distribute dye+buffer from either a 15 mL tube/12-row trough to every well of a 96-well plate, and (2) transfer 2 uL of RNA from 96-well plate to the plate. The RNA plate is maintained at 4°C on a TempDeck. If the 15 mL tube is selected, a P300 single-channel pipette will be required; otherwise, the protocol will call for a P300 multi-channel.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [TempDeck](https://shop.opentrons.com/products/tempdeck)

## Process
1. Select your reagent container type.
2. Input the volume of dye+buffer to be transferred to each well.
3. Input the volume of RNA sample to be transferred to each well.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will transfer dye+buffer to each well using a P300 pipette.
10. Robot will transfer RNA to each well using a P10 multi-channel pipette.

### Additional Notes
Setup
* Receptor Plate: Slot 1
* 15 ml Tube Rack/12-row Trough: Slot 2
* RNA Plate on TempDeck: Slot 4

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
qNSHMgnB
1223

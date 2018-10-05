# Alternate Sample Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
With this protocol, your robot can distribute two reagents from a 2-column reagent trough to two separate 96-well plates using a P300 multi-channel pipette. Samples will be transferred from a deep well block to the plate with reagent 1 using a P50 multi-channel pipette. Plate 1 will then be transferred to plate 2. Lastly, content of plate 2 will be transferred to PCR strips on the Temperature Module.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will distribute 50 uL/well of Reagent 1 across microtiter plate 1 (slot 4).
7. Robot will distribute 45 uL/well of Reagent 2 across microtiter  plate 2 (slot 5).
8. Robot will transfer and mix 25 uL/well of samples from deep well block to microtiter plate 1 column-by-column, using new tips for each transfer.
9. Robot will transfer 5 uL/well from microtiter plate 1 to microtiter plate 2 column-by-column, using new tips for each transfer.
10. Robot will transfer 30 uL from microtiter plate 2 to PCR tubes on the Temperature Module.

### Additional Notes
* 2-Column Trough Setup:
    * A: Reagent 1
    * B: Reagent 2

###### Internal
XdfIDw2i
1101

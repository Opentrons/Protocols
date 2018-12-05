# Sample Aliquotting

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Distribution

## Description
Using this protocol, your robot will aliquot samples from a single 1.5 mL tube to up to 239 empty 1.5 mL tubes. This protocol would require our [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1). User can change the aspirate and dispense speeds for solutions with various viscosity.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input the number of aliquots you would like to create.
2. Input the desired aspirate and dispense speed (UNIT: uL/sec; DEFAULT: aspirate=25, dispense=50).
3. Input the aliquot volume.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will aliquot your sample in well A1 of tube rack in slot 1 to the rest of the tubes.

### Additional Notes
Your sample is *always* in well A1 of the tube rack in slot 1.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
aFcFupuB
1437

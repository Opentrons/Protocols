# NGS Library Prep - D700 Transfer

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs a D700 distribution from 200ul PCR strips to a ThermoFisher 96-well MicroAmp EnduraPlate mounted on a temperature deck set at 4˚C. The user can select parameters such that this protocol fulfills parts 5uL D700 1, 5uL D700 2, and 5uL D700 3 (parts 6, 7, and 8, respectively) of the NGS prep.

---

You will need:
* [P10 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [ThermoFisher 96-Well MicroAmp EnduraPlate #4483348](https://www.thermofisher.com/order/catalog/product/4483348)
* 96 200µl PCR strips

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Input the transfer volume, D700 strip column, and destination column. Ensure the PCR plate is mounted on the temperature deck before running.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The temperature deck with mounted plate heats to 4˚C before the protocol begins.
8. The specified volume of D700 is transferred to the specified destination column. Tips are discarded.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Yp5gMvur
1549

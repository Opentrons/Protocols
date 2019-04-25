# NGS Library Prep - Mix Distribution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs a mix distribution from 200ul PCR strips to a ThermoFisher 96-well MicroAmp EnduraPlate mounted on a temperature deck set at 4˚C. The user can select parameters such that this protocol fulfills 10uL Random Priming Mix, 3uL Exo rSAP MM, 10.5uL Adaptase, and 25.3uL Indexing D500 (parts 1, 2, 4, and 5, respectively) of the NGS prep. The multi-channel pipette that is needed is automatically determined by the protocol after the user inputs the desired transfer volume.

---

You will need:
* [P10 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P50 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Zymo-Spin I-96 Plate #C2004](https://www.zymoresearch.com/products/zymo-spin-i-96-plate)
* [ThermoFisher 96-Well MicroAmp EnduraPlate #4483348](https://www.thermofisher.com/order/catalog/product/4483348)
* 96 200µl PCR strips

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Input the transfer volume, mix strip column, destination columns start, and number of columns to fill, and whether or not to mix after each transfer. Ensure the PCR plate is mounted on the temperature deck before running.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The temperature deck with mounted plate heats to 4˚C before the protocol begins.
8. The specified volume of mix is transferred to each specified column, using new tips each time. The destination columns on the temperature deck plate are mixed after the transfer if specified as such.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Yp5gMvur  
1549

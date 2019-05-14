# Custom Cassette Plate Filling

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol performs a liquid transfer from 13 source tubes mounted on an aluminum block mounted on a temperature deck. Each substance is transferred to its corresponding well on each of 9 custom 2x12 cassettes. See 'Additional Notes' below for reagent setup.

---

You will need:
* [P1000 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [1000µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* 96-well Flat PCR plate

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module with aluminum block set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. For each of 13 reagent tubes mounted on the temperature module with aluminum block, 100ul of reagent is distributed to its corresponding well on each of 9 custom cassettes. New tips are used for each substance distribution (13 tips total).

### Additional Notes
![Tube Setup on Aluminum Block](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1572/tube_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
X7R4hMHw  
1572

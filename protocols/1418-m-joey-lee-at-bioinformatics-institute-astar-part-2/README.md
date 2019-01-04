# 96 to 384 WP mapping

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Mapping

## Description
With this protocol, your robot will map serial dilutions from a 96 well plate to a 384 well plate as shown in Additional Notes.

---

To run this protocol, you will need:
* P10 Single-channel Pipette
* p50 or p300 Multi-channel Pipette
* Single Channel Trough
* [Corning 384-well Microplates](https://www.sigmaaldrich.com/catalog/product/sigma/cls3575?lang=en&region=US)
* [Opentrons 300 uL Tip Racks](https://shop.opentrons.com/collections/opentrons-tips)
* 10 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will use multichannel to distribute serial dilution results to a 384 well plate as shown
7. Robot will use single channel to fill in remaining wells


### Additional Notes
Moving from left to right, the samples decrease in concentration until reaching the C1 reagent columns.
For the second set of columns, the lowest concentration of sample is not plated.

After the samples are plated with the multichannel, the single channel will distribute to all wells that do not go down
the whole column of the 384 well plate. This is applicable for rows 17-23.
---

There is one custom variable with this protocol as follows:
transfer_volume, default is 20uL. If you specify an amount greater than or equal to 50uL the protocol will utilize a 300uL multichannel pipette. Otherwise, it will use a 50uL multichannel.

![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1418-m-joey-lee-at-bioinformatics-institute-astar/plate_layout_384.JPG)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
wrq0Mbg0
1418

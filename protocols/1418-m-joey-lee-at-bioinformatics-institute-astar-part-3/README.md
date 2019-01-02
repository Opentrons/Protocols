# Protein-based Compound Screening

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Distribution

## Description
With this protocol, your robot can transfer reagent from a single channel trough to all wells designated in Additional Notes

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
6. Robot will transfer X amount of reagent to all wells specified by layout

### Additional Notes
There is one custom variable with this protocol as follows:
transfer_volume, default is 20uL. If you specify an amount greater than or equal to 50uL the protocol will utilize a 300uL multichannel pipette. Otherwise, it will use a 50uL multichannel.

As mentioned previously, the reagent will be loaded into the 384 well plate in all wells with a designated sample.
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1418-m-joey-lee-at-bioinformatics-institute-astar/plate_layout_384.JPG)
---

Before the start of protocol, pre-load your compounds in plate 1 this way:
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1416-quentis-therapeutics/plate_1.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
KMdSdj6k
1416

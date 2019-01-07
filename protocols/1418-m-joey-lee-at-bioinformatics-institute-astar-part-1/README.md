# Serial Dilution A

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Serial Dilution

## Description
With this protocol, your robot will load a 96 well plate with samples using a p10 single channel and the opentrons tuberack. Then, using a mulichannel it will add reagent from a single channel trough into the designated columns. From there, the multichannel will perform a serial dilution across the columns of the plate.

---

To run this protocol, you will need:
* P10 Single-channel Pipette
* p300 Multi-channel Pipette
* Single Channel Trough
* Opentrons 4-in-1 tuberack
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
6. Robot will distribute samples from a tuberack to the second column of a 96 well plate.
7. Robot will distribute P samples from a tuberack to the 11th column of a 96 well plate.
8. Robot will add reagent from a single channel trough to columns 2-8
9. Robot will serially dilute from column 2->8, mixing before each transfer


### Additional Notes
There are three custom variables for this protocol.
sample_volume: This is the volume to distribute for each sample in column 2. Default is 4.
number_samples: This is the number of samples to be distributed into column 2. Default is 8
reagent_volume: This is the volume of reagent to be added to column 2. Default is 100.

It is assumed that the P samples are pre-loaded.

Please see this
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1418-m-joey-lee-at-bioinformatics-institute-astar/plate_layout_96.JPG)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
wrq0Mbg0
1418

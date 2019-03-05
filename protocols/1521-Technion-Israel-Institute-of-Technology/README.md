# Cell Culture Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Assay

## Description
This protocol performs a liquid transfer for cell cultures and related assays. The protocol allows for a user input volume of medium and volume of sample, as well as number of mixes and delay between mixes after the liquid transfer is complete. For reagent setup, see 'Additional Notes' below.

---

You will need:
* [p300 Multi-channel pipette](https://shop.opentrons.com/collections/ot-one-s-robot-and-accessories/products/ot-hood)
* [p10 Single-channel pipette](https://shop.opentrons.com/collections/ot-one-s-robot-and-accessories/products/p200-single-channel-pipette)
* [10µl tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300µl tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* 2ml tubes
* [2ml tube rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [12-row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

### Robot
* [OT-One S Hood](https://shop.opentrons.com/collections/ot-one-s-robot-and-accessories/products/ot-hood)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. The specified volume of medium is transferred from row A1 of the 12-row trough to each well in the 96-well plate using a p300 8-channel pipette. The same tips are used across the entire transfer and then discarded.
7. The specified volume of sample is transferred from well A1 of the 2ml tube rack to each well of the the plate using a p10 single-channel pipette. The same tip is used across the entire transfer and then discarded.
8. The contents of each well are mixed 3x with the p300 multi-channel pipette using the same tips.
9. The pipette delays for a user specified amount of time.
10. Steps 8 and 9 are repeated as many times as specified.

### Additional Notes
![Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1521-Technion-Israel-Institute-of-Technology/setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
zc8Xq26S  
1521

# Protein Normalization Cherrypicking

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol performs protein sample normalization according to parameters input in a CSV file (see 'Additional Notes' below for example CSV setup). The final dilution plate is mounted on an Opentrons temperature module.

---

You will need:
* [Micronic 96-1 rack](https://s3-ap-southeast-2.amazonaws.com/paperform/u-4256/0/2019-06-28/e113nu4/micronic%2096-1.pdf)
* [Micronic 0.50ml Tubes Internal Thread (seated in Micronic 96-1 rack)](https://www.micronic.com/product/050ml-tubes-internal-thread)
* [USA Scientific 96 Deep Well Plate 2.4 mL # 1896-2000](https://www.usascientific.com/2ml-deep96-well-plateone-bulk.aspx)
* [Agilent 1 Well Reservoir 290 mL # 201252-100](https://www.agilent.com/store/en_US/Prod-201252-100/201252-100)
* [Opentrons P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 10ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 1000ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons temperature module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Upload your CSV and input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The CSV is parsed to determine the number of dilutions and volumes of stock protein and buffer for each dilution.
8. All dilutions are carried out in the corresponding wells of the source, step dilution, and final dilution plates. New tips are used for each proteins sample.

### Additional Notes
[Example CSV file](https://s3-ap-southeast-2.amazonaws.com/paperform/u-4256/0/2019-07-01/pu1344c/Protein%20dilution.xlsx)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
MjXbB2Wu  
1621

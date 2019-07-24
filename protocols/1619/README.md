# Sample Aliquoting

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Distribution

## Description
This protocol performs sample consolidation in a 96-well collection plate mounted on a temperature module and distribution to custom Micronic tuberacks in 8 aliquots per consolidated sample. The 'number of protein samples' input field corresponds to the number of consolidated samples (for example, an input of 24 samples specifies 48 starting wells containing liquid; horizontally adjacent wells are consolidated in the left duplicate well). This input should be a multiple of 8 for compatibility with the Opentrons multi-channel pipette. For transfer schematic, see 'Additional Notes' below.

---

You will need:
* [GE Healthcare V-Bottom 96-Well Collection Plate # 28-4039-43](https://www.sigmaaldrich.com/catalog/product/sigma/ge28403943?lang=en&region=US)
* [Micronic 96-1 rack](https://s3-ap-southeast-2.amazonaws.com/paperform/u-4256/0/2019-06-28/e113nu4/micronic%2096-1.pdf)
* [Micronic 0.50ml Tubes Internal Thread (seated in Micronic 96-1 rack)](https://www.micronic.com/product/050ml-tubes-internal-thread)
* [Opentrons P50 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P300 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [300ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV file and select the mount for your P1000 pipette.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 100ul of up to 48 samples are consolidated in alternating columns, and mixed after (see image 1 below). New tips are used for each sample consolidation.
8. 25ul of each sample is distributed to a column of 8 aliquot tubes in the destination tube racks (200ul total sample distributed). Source samples are taken down each column before moving across the rows. Once all columns of destination tubes of one rack have been filled, destination columns move to the first column of the next plate (see image 2 below). Tips are changed after every sample distribution (1 tip for 8 aliquots).

### Additional Notes
Image 1: initial sample consolidation:  
![initial sample consolidation](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1619/source_plate_scheme.png)

Image 2: aliquotting scheme:  
![aliquot scheme](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1619/aliquot_scheme.png)

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
bW5ZjqSf  
1619

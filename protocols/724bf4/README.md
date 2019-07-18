# PCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs PCR preparation on a custom 384-well destination plate. The protocol samples combinations of 16 primers and 8 cDNA samples. For transfer schematic, please see the file in 'Additional Notes' below.

---

You will need:
* [Roche Lightcycler 384-well plate # 05102430001](https://lifescience.roche.com/en_us/products/lightcycler14301-multiwell-plate-384-clear.html)
* [SSI 0.2ml 8 strip PCR tubes, flat caps # 313500 (seated)](https://www.ssibio.com/pcr/strip-pcr-tubes-and-caps)
* [Opentrons 2ml Eppendorf tube rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Opentrons P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P50 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons 10ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [Omega Biotek Mag-Bind Bacterial DNA 96 Kit # M2350-01](https://www.omegabiotek.com/product/mag-bind-bacterial-dna-96-kit/)

## Process
1. Input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The specified volume of each primer is distributed across each row of the 384-well plate, using new tips for each primer. For specific transfer scheme, please see 'Additional Notes' below.
8. The specified volume of each cDNA is distributed to 3 columns each of the 384-well plate, using new tips for each cDNA. For specific transfer scheme, please see 'Additional Notes' below.

### Additional Notes
[Transfer scheme](https://s3-ap-southeast-2.amazonaws.com/paperform/u-4256/0/2019-07-09/wd13di5/qRT%20PCR%20excel%20.xlsx)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
724bf4

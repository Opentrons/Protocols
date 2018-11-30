# PCR Using TaqPath™ ProAmp™ Master Mixes

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
Your robot can use this protocol to create PCR mixes using the [TaqPath™ ProAmp™ Master Mixes](https://www.thermofisher.com/order/catalog/product/A30865). This protocol is specifically designed for 8 samples and 12 TaqMan Genotyping Assays. A P10 single-channel pipette is required.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* Sterile Water
* [TaqPath™ ProAmp™ Master Mix](https://www.thermofisher.com/order/catalog/product/A30865)
* TaqMan custom fluorescent labeled assays

## Process
1. Input your desired volumes for water, master mix, each assay, and sample.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will use the same tip to distribute water and master mix to all wells of the 96-well plate.
8. Robot will transfer each assay to each column, assay 1 to column 1, assay 2 to column 2, etc.
9. Robot will transfer each sample to each row, sample 1 to row A, sample 2 to row B, etc.

### Additional Notes
Tube Rack Setup
* Samples 1-8: well A1-D2
* Assays 1-12: well A2-D5
* Water: well A6
* Master Mix: well B6

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ZJo0gmcP
1355

# PicoGreen Assay For 384-well Plate

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
This protocol allows your robot to perform the Picogreen Assay on up to 184 samples in a 384-well plate. Samples will be provided by users in up to two 96-well PCR plates. Standards an a blank will be included on the 384-plate. Please see Additional Notes for more information on the setup.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* [Quant-iT™ PicoGreen™ dsDNA Assay Kit](https://www.thermofisher.com/order/catalog/product/P7589)

## Process
1. Input the number of samples you will be running.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 10 uL standards from PCR-strip 1 into column 1 of the 384-well plate in duplicate.
8. Robot will transfer 10 uL PicoGreen reagent from PCR-strip 2 to each standard well.
9. Robot will transfer 19 uL 1xTE buffer and PicoGreen reagent mix from reservoir well A1 into the designed sample wells on the 384-well plate, starting at column 2, up to column 24.
10. Robot will transfer 1 uL sample into its designed well. columns 1-12 of the first sample plate will go to column 2-13, and columns 1-11 of the second sample plate will go into column 14-24 in the 384-well plate.

### Additional Notes
384-well Plate Layout
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1443-university-of-technology-sydney/layout.png)  
* Column 1: 4 standards and blank
* Columns 2-24: Up to 184 samples

---

Deck Setup
* Sample Plate 1: slot 1
* 384-well Plate: slot 2
* Sample Plate 2: slot 3
* PCR Strip Tubes: slot 4
* Reagent Trough: slot 5

---

Reagent Trough Setup
* PicoGreen Mix: well A1

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
R5AMPtlV
1443

#  Fluorescence Polarization Enzyme Assay - Antibody Set-Up

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Assay

## Description
This protocol allows your robot to perform a customizable Florescence Polarization Enzyme Assay. Throughout the protocol steps, the same 384 well plate is used until the standard curve step. See Additional Notes for further information on this part.

Links:
* [Part 2: Specific Enzyme Concentration](./1444-s-computing-research-unit-uct-part-2)
* [Part 3: Assay Setup](./1444-s-computing-research-unit-uct-part-3)
* [Part 4: Standard Curve](./1444-s-computing-research-unit-uct-part-4)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* [AMP2/GMP2 Fluorescence Polarization Kit](https://www.bellbrooklabs.com/products/transcreener-hts-assays/amp2-gmp2-phosphodiesterase-assay/amp2-gmp2-fp-assay/)

## Process
1. Input your values into custom fields. See Additional Notes.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer X uL master mix A into rows A,B,C from column 1 to 24.
8. Robot will transfer X uL AB- titrator into the first column and row A,B,C.
9. Robot will transfer X uL of master mix + titrator combination in column 1 and serially titrate across columns.


### Additional Notes
In this part of the protocol, there are four variables.
A.] pipette_type: either p10 single or p50 multichannel
B.] mm_volume: master mix volume, default is 10
C.] titrator_volume: titrator volume, default is 10
D.] dilution_volume: serial dilution volume, default is 10

If you choose a single channel the following will be true:
1. A tuberack will be holding the master mix and AB titrator; these are located in A1 and B1 respectively
2. You only have one substrate Concentration and thus the mastermix/ titrator will only be distributed into the first three rows

If you choose a multi channel the following will be true:
1. A 96 flat plate will be holding the master mix and AB titrator; this will be located in column 1 and 2 respectively
2. For any wells in which you do not wish master mix to be distributed, either do not fill the associated well in the 96 flat or remove tips from the tip box before beginning the protocol.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
jurF616m
1444

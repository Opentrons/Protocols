#  Fluorescence Polarization Enzyme Assay - Standard Curve Set Up

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Assay

## Description
This protocol allows your robot to perform a customizable Florescence Polarization Enzyme Assay. Throughout the protocol steps, the same 384 well plate is used until the standard curve step. See Additionl Notes for further information on this protocol.

Links:
* [Part 1: Antibody Setup](./1444-s-computing-research-unit-uct-part-1)
* [Part 2: Assay Setup](./1444-s-computing-research-unit-uct-part-2)
* [Part 3: Standard Curve](./1444-s-computing-research-unit-uct-part-3)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* [AMP2/GMP2 Fluorescence Polarization Kit - Bellbrooks Laboratories](https://www.bellbrooklabs.com/products/transcreener-hts-assays/amp2-gmp2-phosphodiesterase-assay/amp2-gmp2-fp-assay/)

## Process
1. Input the number of samples you will be running.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer master mix e into column 1->3 up to amount of changing donor substrate they have
8. Robot will transfer dectection reagent into all necessary wells and mix

### Additional Notes
There are four custom variables in this protocol.
A.] pipette_type: either a p10 singlechannel or p50 multichannel
B.] standards: number of standards required with a maximum of 12. Default is 12.
C.] standard_volume: volume of standard to be distributed. Default is 15
D.] detection_reagent_volume: volume detection reagent to be distributed to same wells as standards. Default is 5.

For the multichannel, the master mix should be placed in the first column of the 96 WP and the detection reagent should be placed in the second column.
For the singlechannel, the master mix should be placed in the tuberack at wells A1 and B1.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
jurF616m
1444

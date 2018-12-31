#  Fluorescence Polarization Enzyme Assay - Specific Enzyme Concentration

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Assay

## Description
This protocol allows your robot to perform a customizable Florescence Polarization Enzyme Assay. Throughout the protocol steps, the same 384 well plate is used until the standard curve step. See Additionl Notes for further information on this protocol.

Links:
* [Part 1: Antibody Setup](./1444-s-computing-research-unit-uct-part-1)
* [Part 3: Assay Setup](./1444-s-computing-research-unit-uct-part-3)
* [Part 4: Standard Curve](./1444-s-computing-research-unit-uct-part-4)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* [AMP2/GMP2 Fluorescence Polarization Kit](https://www.bellbrooklabs.com/products/transcreener-hts-assays/amp2-gmp2-phosphodiesterase-assay/amp2-gmp2-fp-assay/)

## Process
1. Input the number of samples you will be running.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer X uL of master mix c,d,e to rows I,K,M,O
8. Robot will transfer titrator to first column of 384 in those rows
9. Robot will do a serial dilution across rows I, K, M, O mixing along the way
10. Robot will distribute detection reagent to all wells in rows I,K,M,O mixing along the way

### Additional Notes
There are 8 separate variables to choose from for this part of the protocol
A.] pipette_type: either p10 single or p50 multichannel
B.] mm_volume: volume used for master mix c,d,e, default 10ul
C.] mm_location: starting location for a master mix; This should be the _column_ that the mastermixes would be located in. If in a tuberack, it would start the tubes at row A and move down the given column for the rest of the master mixes. Range is from *1-6* for single channel and *1-12* for the multichannel 
D.] titrator_location: location for the titrator reagent; This should be *either* a _column_ of a 96 WP or a _well_ of the tuberack. Range is from *A1-D6* for single channel and *1-12* for the multichannel
E.] titrator_volume: volume used for titrator, default 10ul
F.] dilution_volume: volume used for dilution of detection reagent, default 10ul
G.] detection_reagent_volume: volume of dectection reagent distributed to 384 well plate
H.] incubation_time: time (in minutes) for RT incubation

###### Internal
jurF616m
1444

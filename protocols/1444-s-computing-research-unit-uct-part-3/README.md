#  Fluorescence Polarization Enzyme Assay - Running the Assay

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
7. Robot will transfer X uL of master mix e to designated locations
8. Robot will transfer X uL of donor substrate to the same designated locations and mix

### Additional Notes
There are eight custom variables for this part as follows:
A.] mm_volume: volume of master mix e. Default is 10,
B.] donor_sub_volume: volume of donor substrate. Default is 10,
C.] start: the starting row or column to distribute to. Default is 'A'. If single channel, the range is *'A'-'P'* or if multichannel, the range is *'1'-'24'*
D.] end: the ending row or column to distribute to. Default is 'A'. If single channel, the range is *'A'-'P'* or if multichannel, the range is *'1'-'24'*
E.] starting_well: the starting well _within_ a row that you would like to distribute to. Default is 0, the range is *0-24* for a single channel. For a multichannel you *MUST* input 0.
F.] ending_well: the ending well _within_ a row that you would like to distribute to. Default is 12, the range is *0-24* for a single channel. For a multichannel you *MUST* input 0.
G.] mm_loc: The location of master mix e. Default is 'A1'. The range is *A1-D6* if single channel or *1-12* if multichannel
H.] donor_loc: The location of the donor substrate. Default is 'B1'. The range is *A1-D6* if single channel or *1-12* if multichannel

For the multichannel, if there are *rows* that you wish to skip, you must remove the tips from the tip rack prior to running this protocol OR do not fill the corresponding wells of the 96 WP. Otherwise use the single channel.


If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
jurF616m
1444

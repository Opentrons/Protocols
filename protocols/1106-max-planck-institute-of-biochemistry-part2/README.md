# DNA Origami Part 2/2: Create Folding Mixes

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * DNA Origami

## Description
Part 2 of 2: Create Folding Mixes

Links: [Create Pool Libraries](./1106-max-planck-institute-of-biochemistry-part1) [Create Folding Mix ](./1106-max-planck-institute-of-biochemistry-part2)

This protocol is developed for generating DNA nano-structures (DNA origami). This protocol consists of 2 parts, where part I creates the pool libraries and part II uses the pool libraries to create folding mixes.

In this workflow, the robot can generate up to 10 folding mixes in 0.2 PCR tubes using the pool libraries created previously. Other than the pool libraries, 4 other reagents (Folding Buffer, Scaffold Strand, water, and dye-conjugated strands) will be added to each folding mix. The folding mix information will be provided by user in the form of a CSV. See Additional Notes for the required layout for the CSV.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your folding mix scheme CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer and mix each component into the first PCR tube.
8. Robot will repeat step 7 until all the folding mixes have been made.

### Additional Notes
* Tuberack Layout (slot 1):
    * A1-C3: Pool libraries
    * A6: Biotinylated DNA
    * B6: Folding Buffer
    * C6: H2O
    * D6: Scaffold

* Folding Mix Scheme CSV Layout:
    * Each row represents one folding mix
    * Make sure the header names are spelled correctly

![structure scheme csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1106-max-planck-institute-of-biochemistry/structure_scheme_csv.png)


###### Internal
nmYJZi00
1106

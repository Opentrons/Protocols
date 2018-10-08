# DNA Origami Part 1/2: Create Pool Libraries

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * DNA Origami

## Description
Part 1 of 2: Create Pool Libraries

Links: [Create Pool Libraries](./1106-max-planck-institute-of-biochemistry-part1) [Create Folding Mix ](./1106-max-planck-institute-of-biochemistry-part2)

This protocol is developed for generating DNA nano-structures (DNA origami). This protocol consists of 2 parts, where part I creates the pool libraries and part II uses the pool libraries to create folding mixes.

In this workflow, the robot can pool up to 11 libraries from plate 1 to plate 8. Each library can contain up to 192 Oligos. The robot will prompt the user to replace the two tipracks on the robot between the generation of each library. The pooling information will be provided by the user in the form of a CSV. See Additional Notes for the required layout for the CSV.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your pool scheme CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will pool each component specified in the CSV for the first library.
8. Robot will pause for user to reset the tips.
9. Robot will repeat steps 7-8 until all the libraries are created.

### Additional Notes
* Pool Scheme CSV Layout:
    * Each column represents one pool library
    * First row is **always** the volume to be transferred from each well in uL
    * The source well is presented by ***plate:well***
        * Plate identifier: A-H before the first underscore represents plate 1-8
    ![pool scheme csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1106-max-planck-institute-of-biochemistry/pool_scheme_csv.png)


###### Internal
nmYJZi00
1106

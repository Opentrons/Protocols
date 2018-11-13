# Nextera XT DNA Library Prep Kit Protocol: Part 2/4 - Clean Up Libraries

### Author
[Opentrons](http://www.opentrons.com/)

### Partner
[CosmosID](http://www.cosmosid.com/)

## Categories
NGS Library Prep

## Description
Part 2 of 4: Clean Up Libraries

Links: 
[Part 1: Tagment and Amplify](./872-cosmosid-ngs-library-prep-part1) 
[Part 2: Clean Up Libraries](./872-cosmosid-ngs-library-prep-part2) 
[Part 3: Normalize Libraries](./872-cosmosid-ngs-library-prep-part3) 
[Part 4: Pool Libraries](./872-cosmosid-ngs-library-prep-part4)

With this protocol, your robot can perform the Nextera XT DNA Library Prep Kit protocol describe by the [Illumina Reference Guide](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_nextera/nextera-xt/nextera-xt-library-prep-reference-guide-15031942-03.pdf).

This is Part 2 of the protocol, which consists of just step (3) of the overall process: clean up libraries. This step uses AMPure XP beads to purify the library DNA and remove short library fragments after the previous step, library amplification.

After this step, it is safe to stop the workflow and return to it at a later point. If you are stopping, seal the plate and store at -15°C to -25°C for up to seven days.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://opentrons.com/modules)

### Reagents
* [Nextera XT DNA Library Prep Kit](https://www.illumina.com/products/by-type/sequencing-kits/library-prep-kits/nextera-xt-dna.html)
* [Ampure XP for Size Selection](https://www.beckman.com/reagents/genomic/cleanup-and-size-selection/pcr)

## Process
1. Input your number of samples (make sure it is consistent with what you entered in Part 1).
2. Input your desired volume of the PCR product.
3. Input your desired bead ratio (use 1.8 if the input size is in the range 300-500 bp, use 0.6 if greater 500 bp).
4. Input your desired dry time.
5. Download your protocol.
6. Load your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack, and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".

### Additional Notes
* Trough Setup:
    * Resuspension Buffer: **A1**
    * AMPure XP Beads: **A2**
    * 80% Ethanol: **A3**
* Review the reference guide before proceeding to confirm kit contents and make sure you have the required equipment and consumables.

###### Internal
bU7eUGEh
872

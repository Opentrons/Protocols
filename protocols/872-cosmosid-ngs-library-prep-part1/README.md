# Nextera XT DNA Library Prep Kit Protocol: Part 1/4 - Tagment Genomic DNA and Amplify Libraries

### Author
[Opentrons](http://www.opentrons.com/)

## Categories

## Description
Part 1 of 4: Tagment Genomic DNA and Amplify Libraries

Links: [Part 1](./873-cosmosid-ngs-library-prep-part1) [Part 2](./873-cosmosid-ngs-library-prep-part2) [Part 3](./873-cosmosid-ngs-library-prep-part3) [Part 4](./873-cosmosid-ngs-library-prep-part4)

With this protocol, your robot can perform the Nextera XT DNA Library Prep Kit protocol describe by the [Illumina Reference Guide](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_nextera/nextera-xt/nextera-xt-library-prep-reference-guide-15031942-03.pdf).  

This is part 1 of the protocol, which includes the steps (1) Tagment Genomic DNA and (2) Amplify Libraries. Tagment Genomic DNA uses Nextera transposome to fragment DNA and subsequently tags the DNA with adapter sequences. Amplify Libraries increases the yield of the tagmented DNA using PCR. PCR adds the Index 1 (i7), Index 2 (i5), and full adapter sequences to the tagmented DNA from the previous step.

It is a safe stopping point after these two steps. If you are stopping, seal the plate and store at 2°C to 8°C for up to 2 days. Alternatively, leave on the thermal cycler overnight.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* [Nextera XT DNA Library Prep Kit](https://www.illumina.com/products/by-type/sequencing-kits/library-prep-kits/nextera-xt-dna.html)

## Process
1. Input your number of samples.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
* 2-mL Tuberack Setup
    * Amplicon Tagment Mix: **A1**
    * Tagment DNA Buffer: **B1**
    * Neutralize Tagment Buffer: **C1**
    * Nextera PCR Master Mix: **D1**
    * Index 1 (i7) adapters: **A2-D3**
    * Index 2 (i5) adapters: **A5-D6**
* If number of samples is less than 25, arrange 6 tubes of index 1 (A2-B3) and 4 tubes of index 2 (A5-D5) in the tuberack. Otherwise, fill Index 1 and Index 2 according to the tuberack setup as instructed above.
* Review the reference guide before proceeding to confirm kit contents and make sure you have the required equipment and consumables.

###### Internal
bU7eUGEh
872

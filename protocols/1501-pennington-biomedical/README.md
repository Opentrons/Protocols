# Pennington Biomedical BCA Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Protein and Proteomics
    * BCA Assay

## Description
With this protocol, your robot can perform a bicinchoninic acid (BCA) assay for up to 32 samples in triplicate on a single 96-well PCR plate. Each set of triplicate samples are arranged next to each other horizontally (ex: A1, A2, A3). Subsequent samples in triplicate are filled down the column before moving 3 columns over (ex: sample 1- A1, A2, A3; sample 2- B1, B2, B3; ...; sample 8- H1, H2, H3; sample 9- A4, A5, A6, ...).

---

You will need:
* 4x6 2ml microcentrifuge tube racks
* 200ul tip racks
* 12-row trough
* 96-well PCR plate
* P300 Single-channel pipette
* P300 Multi-channel pipette

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* [Assay kit](http://tools.thermofisher.com/content/sfs/manuals/MAN0011430_Pierce_BCA_Protein_Asy_UG.pdf)

## Process
1. p300-Single pipette distributes 30ul each of triplicates of sample from tube rack to 96 well plate, aligning triplicates of the same sample horizontally adjacent. The pipette tip is discarded.
2. This process is repeated n times for n samples as input by the user. Subsequent samples fill down the column before starting a new set of samples 3 columns over. Tips are changed between each sample transfer.
3. p300-Multi pipette 200ul of solution from the first column of the 12-row trough to the first column of the 96-well plate. The contents are mixed 3x, and the tips are discarded.
4. This process is repeated across the trough and plate until all sample triplicates have received solution.

### Additional Notes

![deck setup](https://s3-ap-southeast-2.amazonaws.com/paperform/u-4256/0/2019-02-06/no134rs/OT2%20Layout%20-%20BCA%20Assay%20Protocol%20Development_Mey%20Feb%202019.jpg)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
1501

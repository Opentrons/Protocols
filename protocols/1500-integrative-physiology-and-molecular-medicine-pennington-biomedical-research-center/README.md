# Pennington Biomedical Colorimetric Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Protein & Proteomics
    * Assay

## Description
With this protocol, your robot can perform a colorimetric acid assay for up to 32 samples in triplicate on a single 96-well PCR plate. Each set of triplicate samples are arranged next to each other horizontally (ex: A1, A2, A3). Subsequent samples in triplicate are filled down the column before moving 3 columns over (ex: sample 1- A1, A2, A3; sample 2- B1, B2, B3; ...; sample 8- H1, H2, H3; sample 9- A4, A5, A6, ...). See additional notes below.

---

You will need:
* 4x6 2ml microcentrifuge tube racks
* 200ul tip racks
* [12-row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* 96-well PCR plate
* P300 Single-channel pipette
* P300 Multi-channel pipette

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* [Assay kit](https://www.caymanchem.com/pdfs/700190.pdf)

## Process
1. p300-Single pipette distributes 175ul each of triplicates of sample from tube rack to 96 well plate, aligning triplicates of the same sample horizontally adjacent. The pipette tip is discarded.
2. This process is repeated n times for n samples as input by the user. Subsequent samples fill down the column before starting a new set of samples 3 columns over. Tips are changed between each sample transfer.
3. p300-Multi pipette 50ul of solution from the first column of the 12-row trough to the first column of the 96-well plate. The contents are mixed 3x, and the tips are discarded.
4. This process is repeated across the plate until all sample triplicates have received solution from trough column 1.
5. Steps 3 and 4 are repeated with trough column 12 to complete the assay.

### Additional Notes

![Sample transfer schematic](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1501-pennington-biomedical/transfer_schematic.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
qT4pYTkP  
1500

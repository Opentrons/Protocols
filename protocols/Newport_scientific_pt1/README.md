# Quantitative LCMS Bioassay: Part 1/2

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
Part 1 of 2: Quantitative LCMS Bioassay

Links: [Part 1](./Newport_scientific_pt1) [Part 2](./Newport_scientific_pt2)

This protocol consists of part I and II, where part I creates the incubation plates depending on the number of samples in the experiment, and part II transfer the incubation plates into PP plates and B-Gone plates. The incubation plates, PP plates and B-Gone plates are separated into 2 sections: reagent wells (A1-B4) and sample wells.


### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".  

Part I: Before Incubation
6. Transfer 50 uL of buffer to both reagent and sample wells of incubation plates.
7. Transfer 40 uL of enzyme to reagent wells A2-B4 and all sample wells.
8. Transfer 20 uL of internal standard to both reagent and sample wells.
9. Transfer 40 uL of water to reagent well A1.
10. Transfer 20 uL of MeOH to reagent wells A3 and B2, and all sample wells.
11. Transfer 20 uL of Gluc Std to reagent wells A1 and A2.
12. Transfer 20 uL of Std 1-10 to reagent wells A4-B10 respectively.
13. Transfer 200 uL of naive solution to reagent wells A1-B1.
14. Transfer 200 uL QC Low, Mid and High to reagent wells B2-B4 respectively.
15. Transfer 200 uL of samples from the sample plate to their corresponding sample wells, and to B4, using a new tip for each sample.

Part II: After Incubation
16. Transfer 300 uL of MeOH to PP plates.
17. Transfer 150 uL of MeOH to PP Plates.
18. Transfer 150 uL from each well of the incubation plates into corresponding well in the PP plates, using a new tip for each transfer.
19. Transfer 133 uL of MeOH to B-Gone plates.
20. Transfer 200 uL from each well of the incubation plates into the B-Gone plates, using a new tip for each transfer.

### Additional Information
* Only if the sample number is greater than 72, a second incubation plate, PP plate and B-Gone plate is needed. Otherwise, all the reagents and samples are dispensed into one plate for each process.
* When the sample number is greater than 72, user can modify which two rows to put the reagents in the incubation, PP and B-Gone plate. If reagent_row_1 is 0, reagents will be stored in row A, and B. If reagent_row_1 is 2, they will be stored in row C, and D, and so on.


###### Internal
aAJeSyVX
1078

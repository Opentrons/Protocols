# Nucleic Acid Normalization in 0.5 mL Tubes Using CSV Input

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
With this protocol, your robot will be able to perform dilutions on 72 samples by diluting each sample from a 1.5 mL micro-centrifuge tube in a (0.5 mL screwcap tube)[https://us.vwr.com/store/product/4674084/vwr-screw-cap-microcentrifuge-tubes]. The volumes of each dilution will be provided in the form of a CSV file. Please see Additional Notes for the CSV formatting requirements.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your dilution CSV.
2. Input the total volume of diluent in the 50 mL conical tube. (We recommend always having more than enough volume of diluent in the conical tube.)
3. Select whether or not you would like to mix the sample in after each transfer.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will transfer the defined volume of diluent into each well.
10. Robot will transfer the defined volume of each sample into each destination well.

### Additional Notes
Samples setup(1.5 mL Eppendorf tubes)
1. Slot 1: Well A1-H12
2. Slot 2: Well A1-H12
3. Slot 3: Well A1-H12

Dilution Outputs setup(0.5 mL Screwcap tubes)
1. Slot 4: Well A1-H12
2. Slot 5: Well A1-H12
3. Slot 6: Well A1-H12Â

![csv setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1327-van-andel-research-institute/csv_layout.png)  
* Column 1: Sample Volume (uL)
* Column 2: Diluent Volume (uL)
* Each row represents a well
* Order of the well goes from from A1-H12 from slot 1-3 (samples), 4-6 (outputs)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
NOg7c4Od
1327

# Plate Normalization and Consolidation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to perform normalization of concentration to a chosen concentration and volume from one plate to a new plate, using the information from the csv file uploaded by the user. The new plate is then consolidated into a single mixtube, depending on the volumes given by the user in a separate csv file. The mixtube is aliquoted into a desired number of tubes and using a user-defined volume. See the formats of the csv files in Additional Notes.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your normalization csv.
2. Upload your consolidation csv.
3. Select the number of aliquots and the volume to be transferred to each tube.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".

### Additional Notes
* Normalization csv format:
    * make sure the headings are the same as:
        * Well: source and destination well
        * Oligo Name
        * Product no.
        * Conc (uM)
        * Volume (ml)
        * Amount (nmol)  

![normalization_csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/plate_normalization/normalization_csv_example.png)


* Consolidation csv format:
    * grid: 8 rows, 12 columns
    * volumes in uL

![consolidation_csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/plate_normalization/consolidation_csv_example.png)

###### Internal
aR5bhEG2
927

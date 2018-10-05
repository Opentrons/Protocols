# Multiplexing: Cherrypicking Samples and Consolidate to One sample

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol allows your robot to cherrypick from up to three 96-well PCR plates into a single 2 mL tube by input three separate CSVs. See Additional Notes for the required csv layout.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload Plate 1 CSV.
2. Upload Plate 2 CSV (optional).
3. Upload Plate 3 CSV (optional).
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".

### Additional Notes
* CSV Layout:
    * Column 1: Well
    * Column 2: Volume to be transferred

    ![csv layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1302-university-of-utah/csv_layout.png)


###### Internal
8eI0OQ8i
1302

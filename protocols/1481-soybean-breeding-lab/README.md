# DNA Dilution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
Your robot can perform DNA dilution by transferring specified volumes of water and DNA into a single well. This protocol allows your robot to dilute DNA from a 96-deep well block in a 96-well PCR plate. Volumes will be uploaded by user as a CSV file in the field below. See Additional Notes for more details on the CSV layout. Water is stored in a 1-well reagent reservoir, measure and input the depth of the well in the custom field below.

---

You will need:
* P10 Single-channel Pipette
* P300 Single-channel Pipette
* [Reagent Reservoir without Lid](http://www.excelscientific.com/texan_content.html)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input the depth (in mm) of the reagent reservoir.
2. Upload the volume CSV.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will distribute water into the destination wells.
9. Robot will transfer each sample into the destination well.


### Additional Notes
CSV Layout:

![csv_example](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1481-soybean-breeding-lab/CSV_example.png)

* Keep the headers
* Well represents both the DNA stock and the output
* Volumes will automatically be rounded up to 1 decimal point

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
TKoe1SWU
1481

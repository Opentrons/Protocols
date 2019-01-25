# DNA Dilution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
Your robot can perform DNA dilution by transferring specified volumes of water and DNA into a single well. This protocol allows your robot to dilute DNA from a 96-deep well block in a 96-well PCR plate. Water is stored in a 1-well reagent reservoir. Volumes to be transferred will be uploaded by user as a CSV file in the field below. See Additional Notes for more details on the CSV layout.

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
1. Upload the volume CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will distribute water into the destination wells.
8. Robot will transfer each sample into the destination well.


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

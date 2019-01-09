# Cherrypicking with CSV Spreadsheet

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Well-to-well Transfer

## Description
This protocol allows your robot to perform cherrypicking on up to 6 plates of a variety of labware types by a CSV input. See Additional Notes to read more on the required CSV format.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select the pipette size, pipette mount and the type of tiprack.
2. Upload your `container CSV`.
3. Upload your `transfer info CSV`.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".


### Additional Notes
![container_csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1467-glenmark-pharmaceuticals/container_csv.png)

* Keep the headers and make sure the spellings of the container are correct:
    * 24-well-plate
    * 24-deep-well
    * 96-flat
    * 96-PCR-flat
    * 96-deep-well
    * 384-plate
    * trough-12row
* Visit our API doc [here](https://docs.opentrons.com/labware.html#opentrons-containers) to see a list of pre-defined containers you could use with this protocol.
* You can only load 6 plates in slot 1-6 in each run.

---
![transfer_info_csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1467-glenmark-pharmaceuticals/transfer_info_csv.png)

* Keep the headers
* Each row represents one single transfer
* While using a multi-channel pipette, `A1` would represents the entire column 1
* If `Yes` is selected, the pipette would mix 3 times at the source well
* Note that you cannot use the multi-channel pipette with a plate in a 24-well format

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Bq05JRKZ
1467

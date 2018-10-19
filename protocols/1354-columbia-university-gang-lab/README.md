# Cherrypicking from Multiple Sources using CSVs

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol allows the robot to create up to 4 different samples by consolidating wells from multiple 2-mL tuberacks and 96 deep-well plates. User will need upload a CSV for each sample they would like to create. Each CSV will need to contain information of the wells from which to be picked. See Additional Notes for the format of the CSVs. This protocol requires the P10 single and P300 single-channel pipettes.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your CSVs.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer and mix the first reagent in the CSV for sample 1 to sample 1 tube.
8. Robot will repeat step 7 until all the reagents have been transferred.
9. Robot will print "Sample 1 finished mixing."
10. Robot will repeat steps 7-9 until all the samples have been created.

### Additional Notes
* Pipette tip strategy: Always use a new tip between each reagent
* Tips could run out during the protocol. The program will pause and prompt user to replace the tipracks. User can resume the protocol once the tipracks have been refilled.
* Deck setup:
    * Tube Rack 1: slot 4
    * Tube Rack 2: slot 5
    * Plate 1: slot 6
    * Plate 2: slot 7
    * Plate 3: slot 8
    * Plate 7: slot 9
    * Plate 10: slot 10
    * Plate 11: slot 11
* CSV Layout:
    * Make sure you use the correct name of the tube rack as shown below:
    ![csv layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1354-columbia-university-gang-lab/sample_csv.png)


###### Internal
fLrLd6RN
1354

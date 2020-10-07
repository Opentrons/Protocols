# PCR Preparation Cherrypicking

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
With this protocol, your robot can perform a custom PCR preparation using a P20-multi pipette.

The .csv file should be formatted as shown in [this template](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/7fc7b1/7fc7b1_csv_template.csv), **including headers line**.

All available empty slots will be filled with tipracks, and the user will be prompted to refill the tipracks if all are emptied in the middle of the protocol.

Mastermix should be filled in the first columns of the mastermix plate in as many columns as necessary. The protocol will automatically calculate when the second column should be acccessed for mastermix once the first column has run out of volume, then the third column, etc.

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
7fc7b1

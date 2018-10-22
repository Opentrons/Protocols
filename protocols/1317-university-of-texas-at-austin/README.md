# PCR Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR

## Description
With this protocol, your robot can perform PCR prep or similar assays using the OT-One. This protocol allows you to easily modify the reagent in the 2 ml tube racks by uploading a tuberack CSV. User will have to define each and every single transfer by uploading another PCR setup CSV. User has the ability to change the total volume of the PCR setup in the field below. See Additional Notes for more details.

### Robot
* [OT-One Standard](https://opentrons.com/robots/ot-one-s-standard)
* [OT-One Pro](https://opentrons.com/robots/ot-one-s-pro)
* [OT-One Hood](https://opentrons.com/robots/ot-one-s-hood)

## Process
1. Upload your tuberack and PCR setup CSVs, and modify the total volume.
2. Download your protocol.
3. Upload your protocol onto the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your tiprack, pipette, plate, and petri dishes using the OT App. For calibration tips, check out our support articles:
 * [Calibrating the Deck](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-deck)
 * [Calibrating the Pipettes](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-pipettes)
6. Hit "Run Job".
7. Robot will transfer mastermix to every destination well defined in the PCR setup.
8. Robot will transfer each reagent defined in the PCR setup to the appropriate wells.

### Additional Notes
Tuberack CSV:  
Column 1: Slot on the deck (A1, or A2), Column 2: Name of reagent, Column 3: Well in the tuberack  
![tuberack csv layout](	https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1317-university-of-texas-at-austin/tuberack_csv.png)
* Well A1 is defaulted to be master mix, skip using well A1 in the CSV.
* You can only use slot A1 and/or A2.
* Make sure to keep the headers.


PCR Setup CSV:  
Column 1: Destination Well, Column 2: Reagent 1 name, Column 3: Reagent 2 name, Column 4: Reagent name 3  
![pcr setup csv](	https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1317-university-of-texas-at-austin/pcr_setup.png)
* The names of the reagents *MUST* match those defined in the Tuberack CSV.
* Make sure you keep the headers.

###### Internal
D5Orzz5u
1317

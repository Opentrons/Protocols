# Bacteriophage Titration

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to perform bacteriophage titration, which determines the number of viral particles in a stock. This process consists of two steps: 4 log dilutions of 8 bacteriophage samples and adding the dilutions to agar plates.

### Robot
* [OT-One](https://opentrons.com/robots)

## Process
1. Input the diameter of the petri dish you are using in the field above.
2. Download your protocol.
3. Upload your protocol onto the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your tiprack, pipette, plate, and petri dishes using the OT App. For calibration tips, check out our support articles:
	* [Calibrating the Deck](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-deck)
	* [Calibrating the Pipettes](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-pipettes)
6. Hit "Run Job".
7. Transfer 297 uL of TSB media to wells A1-H2.
8. Transfer 90 uL of TSB media to wells A3-H6.
9. Transfer and mix 3 uL of each sample to wells A1-H1.
10. Transfer and mix 10 uL of A1-H1 to A2-H2, A2-H2 to A3-H3,... A5-H5 to A6-H6.
11. Transfer 10 uL from A3-D6 onto agar plate 1.
12. Transfer 10 uL from E3-H6 onto agar plate 2.

### Additional Information
* To calibrate your agar plate, position the pipette tip to well A1 (inside of the dish at the bottom left corner). This is how your agar plate should be set up on the deck:  

  ![image](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/agar_plate_orientation.png)

###### Internal
pNnh4Roo
1001

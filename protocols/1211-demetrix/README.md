# Cherrypicking from N Source Plates into 1 or more Destination Plates

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Well-to-well Transfer

## Description
With this protocol, your robot can perform multiple well-to-well liquid transfers using a P10 single channel pipette by parsing through a user-defined CSV. This protocol also allows you to change setup of the robot by uploading a second CSV. See Additional Notes for more details.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your labware CSV and transfer CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer certain volume from the first source well to dest well defined in the transfer CSV.
8. Robot will repeat step 7 until all the transfers have been performed.

### Additional Notes
Labware CSV:  
Column 1: Slot on the deck (1-10), Column 2: Plate Type, Column 3: Custom Container Height  
![labware csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1211-demetrix/labware+csv.png)
* You need to define all of the labware you would use, except for the tipracks.
* [Here](https://andysigler.github.io/ot-api-containerviz/) is a list of pre-defined labware, if you use these, you do not need to define a height
* If you would like to use any custom 96-well and/or 384-well containers, you could make up the plate type. However, you must *MUST* include the number 96 or 384 in the plate type. Otherwise, the program would not recognize those plates.
* You have to use the slots in this order 1, 2, 3, 4,.. up to 10. You *cannot* skip a slot.
* Make sure to keep the headers.

Transfer CSV:  
Column 1: Slot of the Source Plate, Column 2: Source Well, Column 3: Slot of the Destination Plate, Column 4: Destination Well, Column 5: Volume to be transferred  
![transfer csv](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1211-demetrix/transfer_csv.png)
* Both the source slot and dest slot should already be defined in the labware CSV.
* Make sure to keep the headers.

###### Internal
4j7hITxj
1211

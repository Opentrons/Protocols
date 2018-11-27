# Plate Mapping

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Basic Pipetting
	* Plate Filling

## Description
This protocol allows you to map all of the wells in a plate to 1-9 additional plates using an 8-channel pipette.

This protocol can copy one 96 well plate to other 96 well plates, **OR** one 384 well plate to other 384 well plates.
You cannot go 96 to 384, or 384 to 96.

First, the robot will transfer the specified volume from Column 1 of the source plate to Row 1 of all the destination plates. It will change tips, then do the same for Column 2, and so on, until all rows are filled.

### Time Estimate

### Robot
* [Opentrons OT-2](https://opentrons.com/ot2)

### Modules

### Reagents

## Process
1. Input your desired volume into the "transfer volume" field above, and select your source and destination container type. Also input the "Number of destination plates" you want to copy the source plate to.
2. Download your protocol.
3. Upload your protocol into the [OT App](http://opentrons.com/ot-app).
4. Set up your deck according to the deck map image in the app.
5. Calibrate your tiprack, pipette, and labware using the OT app. For calibration tips, check out our [support articles](https://support.opentrons.com/getting-started/software-setup/calibrating-the-pipettes).
6. Click "Run".
7. The robot will pick up one row of tips and dispense your defined volume into each row of the destination containers, and so on for all the rows in the container until all destination containers' rows are filled.

### Additional Notes
* You can get a preview of the action in this [video](https://www.youtube.com/watch?v=AWKfpK9rmuo).
* One row of tips is used throughout the entire run. If you want to implement tip changes or modify your pipette size, see our [API documentation](https://docs.opentrons.com) for tips on how to modify your Python script.



###### Internal

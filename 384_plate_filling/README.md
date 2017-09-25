# 384 Well Plate Filling

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Basic Pipetting
	* Plate Filling

## Description
Easily fill a 384 well plate using a p10 8-channel pipette without tip changes. Use the field labeled "well volume" below to define your preferred volume. You can input any volume from 1-10uL.

## Notes
* One row of tips is used throughout the entire run. If you want to implement tip changes or modify your pipette, see our [API documentation](https://docs.opentrons.com) for tips on how to modify your Python script.

### Time Estimate
4 minutes

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)  
* [OT Hood](https://opentrons.com/ot-one-hood) 

### Modules

### Reagents
* Water

## Process
1. Input your desired volume into the "well volume" field above.
2. Download your protocol.
3. Upload your protocol into the OT App.
4. Set up your deck according to the deck map.
5. Calibrate your tiprack, pipette, and labware using the OT app. For calibration tips, check out our [support articles](https://support.opentrons.com/getting-started/software-setup/calibrating-the-pipettes).
6. Hit run.
7. The robot will pick up one row of tips and dispense your defined volume in each well of the 384 well plate.

### Additional Notes
[Video](https://www.youtube.com/watch?v=AWKfpK9rmuo)



###### Internal

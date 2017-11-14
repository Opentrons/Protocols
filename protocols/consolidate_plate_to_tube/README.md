# Consolidate 96 Well Plate to Microcentrifuge Tube

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Phdbiotech Inc.](http://www.phdbiotech.com/)

## Categories
* Basic Pipetting
	* Plate Consolidation

## Description
With this protocol, your robot can consolidate the contents of an entire 96 well plate into a single 1.5 mL microcentrifuge tube using a p200 single channel pipette, without tip changes. Use this protocol when combining DNA libraries and/or PCR products from an entire plate. This protocol is best suited for consolidations where sterility is not a concern.

### Time Estimate

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)  
* [OT Hood](https://opentrons.com/ot-one-hood) 

### Modules


### Reagents


## Process
1. Input your desired volume into the "consolidate volume" field above. This is the volume that will be pulled from each well of the plate, *not* the total final volume that will go into the tube.
2. Download your protocol.
3. Upload your protocol into the [OT App](http://opentrons.com/ot-app).
4. Set up your deck according to the deck map below.
5. Calibrate your tiprack, pipette, and labware using the OT app. For calibration tips, check out our [support articles](https://support.opentrons.com/getting-started/software-setup/calibrating-the-pipettes).
6. Hit "run".
7. The robot will pick up one tip and aspirate your defined volume from each well of the 96 well plate, transferring that volume from each well into your microcentrifuge tube.

### Additional Notes
* One tip is used throughout the entire run. If you want to implement tip changes, modify your pipette size, or change your labware, see our [API documentation](https://docs.opentrons.com) for tips on how to modify your Python script.



###### Internal

# 384 Well Plate Filling

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Basic Pipetting
	* Plate Filling

## Description
With this protocol, your robot can fill an input number of columns on an input number of 384-well plates (maximum 9) from a source 12-row trough using any sized pipette from p10-p300 (without tip changes). This can be particularly useful for cell culture seeding, PCR master mix distribution, and more!

Use the field labeled `well volume` below to define your preferred volume. You can input any volume from 1-300uL.

You can also select which columns to be filled by defining the `plate starting column`, and `number of columns to fill`. For example, if your `plate starting column` is 2, and `number of columns to fill` is *23*, your robot will dispense the reagent to column *2-24* (well *A2-P24*).

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)  
* [OT Hood](https://opentrons.com/ot-one-hood)

## Process
1. Input your desired volume into the "well volume" field above.
2. Select the well for your reagent in the trough.
3. Input the starting column to fill on the 384-well plate.
4. Input the number of columns to fill in total on the plate.
5. Select your pipette type.
6. Select whether or not you would like to pipette to mix the reagent before aspirating.
7. Input the number of plates to fill.
8. Download your protocol.
9. Upload your protocol into the [OT App](http://opentrons.com/ot-app).
10. Set up your deck according to the deck map.
11. Calibrate your tiprack, pipette, and labware using the OT app. For calibration tips, check out our [support articles](https://support.opentrons.com/getting-started/software-setup/calibrating-the-pipettes).
12. Hit "run".
13. The robot will pick up one row of tips and dispense your defined volume into each well of the each of the 384-well plates, until all specified columns are filled for all plates.

### Additional Notes
* You can get a preview of the action in this [video](https://www.youtube.com/watch?v=AWKfpK9rmuo).
* One row of tips is used throughout the entire run. If you want to implement tip changes or modify your pipette size, see our [API documentation](https://docs.opentrons.com) for tips on how to modify your Python script.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal

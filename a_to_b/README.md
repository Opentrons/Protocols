# Sample Transfer Setup

### Author
[Opentrons](https://opentrons.com/)

### Partner


## Categories
* Basic Pipetting
	* Plate Consolidation

## Description
With this protocol, your robot can transfer samples from any source labware to any destination labware at a fixed volume. This is great for workflows involving sample distribution and plate mapping. You can define your pipette, axis, source labware, destination labware, transfer volume, and number of samples using the input fields below. 

### Time Estimate
Varies

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](https://opentrons.com/ot-one-hood)

### Modules


### Reagents


## Process
1. Define the number of channels in your pipette using the _"pipette channels"_ field. Input "1" for a single channel pipette or "8" for an eight channel pipette.
2. Define which [axis](https://support.opentrons.com/hardware-questions/setup/switching-pipettes-between-axes) your pipette is on using the *"pipette axis"* field. Input "a" for the A/center axis or "b" for the B/left axis.
3. Define your source labware by typing in the name of the labware in the *"source container type"* field. For labware naming conventions and a list of labware currently supported by Opentrons, please see our documentation on [containers](http://docs.opentrons.com/containers.html). 
4. Input the maximum volume of your pipette using the *"pipette model"* field. *For example*, if you were using a pipette with a volume range from 20-200uL, you would input "200".
5. Define your destination labware by typing in the name of the labware in the *"destination container type"* field. For labware naming conventions and a list of labware currently supported by Opentrons, please see our documentation on [containers](http://docs.opentrons.com/containers.html). 
6. Define your desired transfer volume using the *"well volume"* field below. This volume will apply to every transfer in this protocol.
7. Define the number of transfers you wish to carry out using the *"number of wells"* field.
8. Download your protocol.
9. Upload your protocol into the [OT App](http://opentrons.com/ot-app).
10. Set up your deck according to the deck map below.
11. Calibrate your tiprack(s), pipette, and labware using the OT app. For calibration tips, check out our [support articles](https://support.opentrons.com/getting-started/software-setup/calibrating-the-pipettes).
12. Hit "run". 
13. The robot will pick up tip(s) from the tiprack and transfer your defined volume from your source labware to your destination labware following "one-to-one" mapping. This means transfers will happen from "A1" in your source to "A1" in your destination, then "B1" to B1", "C1" to C1", etc for the number of transfers you defined in Step 7 above. The robot will change tips between each transfer to maintain sterility between samples. If the transfer volume you defined in Step 6 exceeds the maximum working volume of your pipette, it will get broken up into multiple transfers.


### Additional Notes
* The "well volume" input applies to all samples; therefore, this template will not allow you to transfer variable volumes between wells. If you want to change the volume individually for each transfer action, see our [API documentation](http://docs.opentrons.com/) for tips on how to modify your Python script.

###### Internal

# Dispense Medicine on Cookies

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Industry
	* Capsule Filling

## Description
Your robot will dispense a designated amount of medicine onto up to 18 cookies on the robot's deck. Medicine is positioned on the center of the temperature module in slot 11. Arrangement of cookies is specificed on the included pdf document (2 cookies per slot). The robot dispenses the same volume on all cookies, minimum volume of 5 microliters. The pipette (either p50 or p300 single channel) is determined by the volume. The height below the top of the medicine container can be adjusted based on the liquid level in the medicine container.

### Robot
* OT2


### Reagents
* Medicine (liquid)
* Cookies (1-18)

## Process
1. Input your desired volume into the field above.
2. Input the number of cookies in the field above.
3. Input the height below top of the medicine container (for aspiration) in the field above.
4. Download your protocol.
5. Upload your protocol into the [OT App](http://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Make sure cookies are properly arranged on the robot.
8. Calibrate your tiprack, pipette, and labware using the OT app.
9. Hit "run".

Protocol begins:

10. The robot will pick up one tip and aspirate the defined volume of medicine from the container on the temperature module.
11. The robot will dispense your defined volume onto each cookie.
12. Robot will repeat step 10-11 for the total number of cookies you set earlier.

### Additional Notes
* During calibration, you will only be able to calibrate the left-most cookie in each slot. There are two cookies per slot. Make the that the right-most cookie is positioned correctly using the included pdf.
* If the volume is greater than 300 uL, the robot will execute multiple transfers to reach the necessary volume
* Height of the medicine dispense above the cookie is determined by you during calibration
* Robot starts with the cookies at slot 1. Then is goes to slot 2, 3, 4, etc. Robot ends with the cookies at slot 9.
![cookie arrangement](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/cookie_arrangement.png)

###### Internal
I0N6fEWl
893

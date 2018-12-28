# Sterile Workflow for Six 2-mL Tubes

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows you to run solubilize lyophilized powder in 2 mL tubes to desired concentration by inputting volumes of water using a CSV file. The robot will distribute each tube to 32 wells in a 96-well plate. You can process up to six 2 mL tubes with this protocol. See Additional Notes below for the required CSV format.

### Robot
* [OT-One](https://opentrons.com/robots)

## Process
1. Upload your CSV file.
2. Select the tube rack type you are using.
3. Download your protocol.
4. Upload your protocol onto the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your tiprack, pipette, plate, and petri dishes using the OT App. For calibration tips, check out our support articles:
 * [Calibrating the Deck](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-deck)
 * [Calibrating the Pipettes](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-pipettes)
7. Hit "Run Job".
8. Robot will transfer and mix water from trough to each tube, and transfer each tube to a well in the trough, starting at well A1.
9. Robot will distribute each content of the tube to 32 wells in 96-well plates.
10. Robot will collect the rest of the content in each well of the trough and return it back to the 2 mL tubes.

### Additional Notes
Trough Setup
* Empty: A1-A11
* Water: A12

---

If you have any questions about this protocol, please email protocols@opentrons.com.


###### Internal
hvW40Vj6
1460

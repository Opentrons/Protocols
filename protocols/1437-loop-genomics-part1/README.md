# Mastermix Assembly

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Distribution

## Description
Using this protocol, your robot will transfer solutions between two [deep-well plates](https://www.thermofisher.com/order/catalog/product/AB0787?SID=srch-hj-AB-0787) and then to a desired number of [PCR plates](https://us.vwr.com/store/product/4679497/vwr-96-well-pcr-and-real-time-pcr-plates). User has the ability to define the transfer volumes, the number of PCR plates and the number of columns in the PCR plates to fill.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input your desired master mix volume (volume to transfer from column 1 of deep well plate in slot 6 to that of slot 3, and so on).
2. Input your desired reagent volume (volume to transfer from column 1 of deep well plate in slot 3 to those of the PCR plates, and so on).
3. Input the number of PCR plates you are processing.
4. Input the number of columns to be filled in the PCR plates.
5. Download your protocol.
6. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".
10. Robot will transfer master mix from column 1 of deep well plate in slot 6 to deep well plate in slot 3.
11. Robot will transfer reagent from column 1 of deep well plate in slot 3 to column 1 of PCR plates in the robot.
12. Robot will repeat step 10-11 to fill the rest of the columns that is defined by user.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
aFcFupuB
1437

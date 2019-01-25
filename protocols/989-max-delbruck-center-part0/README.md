# Plate Coating

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Cell Coating

## Description
With this protocol, your robot can perform plate coating. This protocol supports a 24-well plate (max 24 samples/run) or 96-well plate (max 96 samples/run).

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Select your cell container type.
2. Select your pipette model and axis for cell feeding. Note that you can ONLY use single channel pipettes with 24-well plates.
3. Select your reagent container type. Note that you can ONLY use the tube racks with a single channel pipette.
4. Input your desired number of samples.
5. Input the volume of reagent to transfer to each well.
6. Select the tip use strategy for the entire run.
7. Download your protocol.
8. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
9. Set up your deck according to the deck map.
10. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
11. Hit "Run".
12. Robot will transfer reagent from source container to each well of the plate, based on the number of samples you have entered.

### Additional Notes
* Select a pipette that can handle the entire media volume in the least number of transfers to minimize the protocol run time.

###### Internal
dog1ERZJ
989

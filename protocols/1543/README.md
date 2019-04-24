# Reagent Prep from 15 mL or 50 mL Conical Tube

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Distribution

## Description
This protocol allows the robot to perform distribution of a viscous stock solution from a 15-mL or 50-mL conical tube to up to 50 2-mL screwcap sample tubes. The robot will distribute the specified volume of stock from the source tube to specified number of 2-mL sample tubes.

---

You will need:
* P1000 Single-channel Pipette
* [Opentrons 4-in-1 Tube Rack Sets](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 15-mL / 50-mL Conical Tube
* 2-mL Screwcap Tubes
* 1000 uL Tip Rack


### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select the source tube type.
2. Input the starting stock volume in the source tube in mL.
3. Input the desired transfer volume to each sample tube in uL.
4. Input the number of samples you would like to output.
5. Download your protocol.
6. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".


### Additional Notes
Based on your input, the robot is programmed to calculate the number of source tubes you will need to complete your desired output. If more than 1 tube is needed, make sure all of the source tubes you place in the robot have the same amount of starting stock volume.

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
wd3euyv5
1543

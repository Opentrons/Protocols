# Protein Addition

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Sample Prep

## Description
With this protocol, your robot can add a single protein source from 1 or more 1.5 mL screwcap tubes to the first 4 rows (A1-D24) of a 384-well plate.

---

You will need:
* P10 / P50 Single-Channel Pipette
* [Opentrons Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Opentrons Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* 384-well Plate
* Opentrons Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents

## Process
1. Set the temperature of the temperature module.
2. Set the protein volume to be transferred to each well.
3. Select desired mixing speed.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will wait until the temperature module has reached the desired temperature.
10. Robot will transfer and mix protein from 1.5 mL tube to each well.

### Additional Notes
Robot will use the P50 single-channel pipette if the transfer volume is greater than 10 uL, otherwise, it will use the P10.

---

If the total transfer volume is greater than 1.5 mL, the robot will pick protein from the next tube in the aluminum block: B1, C1, D1, A2...D6 and so on.

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
EZ2fM2U7
1491

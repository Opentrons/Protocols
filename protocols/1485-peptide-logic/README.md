# 384-well Plate Serial Dilution: Up to 30 Samples

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Serial Dilution

## Description
With this protocol, the robot can perform serial dilution for up to 30 samples in a 384-well plate.

---

You will need:
* P300 Multi-channel Pipette
* P50 Multi-channel Pipette
* 384-well Plates
* 12-well Trough
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Set the number of samples to be diluted in this protocol.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 50 uL of buffer to column 2-12 and 14-24 in the compound plate.
8. Robot will dilute the preloaded samples in column 1 and 13 down the compound plate, using a new tip for every dilution.

### Additional Notes

* Compound Plate: Slot 1

---

Throughout the protocol, the robot would pause and prompt you to replenish tip racks as the tips are being used up.

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ICOpTNL5
1485

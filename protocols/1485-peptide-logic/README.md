# 384-well Plate Serial Dilution: Up to 30 Samples

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Serial Dilution

## Description
With this protocol, the robot can perform serial dilution for up to 30 samples in a 384-well plate. The diluted samples will then be transferred to clean 384-well plates in triplicate. Layout of the samples can be found in Additional Notes.

---

You will need:
* P10 Single-channel Pipette
* P50 Multi-channel Pipette
* 384-well Plates
* 12-well Trough
* Opentrons 10 uL Tip Racks
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. number of samples to be diluted in this protocol.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 50 uL of buffer to column 2-12 and 14-24 in the compound plate.
8. Robot will dilute the preloaded samples in column 1 and 13 down the compound plate.
9. Robot will transfer 5 uL of each diluted sample to a clean cell plate in triplicate.

### Additional Notes
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1485-peptide-logic/layout.png)

* Compound Plate: Slot 1
* Cell Plates: Slot 2, 3, 5, 6, 8, 9

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ICOpTNL5
1485

# Dilution using CSV

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, your robot can perform dilution by diluting the same volume of DNAs with different volume of buffer. The volume of buffer will be provided in the form of a CSV file. The details on the layout of the CSV can be found in Additional Notes below.

---

You will need:
* P10 Multi-channel Pipette
* P300 Single-channel Pipette
* 12-row Trough
* 96-well Plates
* 10 uL Tip Rack
* Opentrons 300 uL Tip Rack

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your buffer volume CSV.
2. Set the DNA volume.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will transfer buffer to all wells in the output plate defined in the CSV file using the P300 single-channel pipette.
9. Robot will transfer each column of the DNA plate to each column of the output plate.


### Additional Notes
CSV Layout:

![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1483-aurora-diagnostics/csv_layout.png)

---

Buffer:
* Trough A1

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
yIkoNMLW
1483

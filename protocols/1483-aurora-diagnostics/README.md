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
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 96-well Plates
* 10 uL Tip Rack
* Opentrons 300 uL Tip Rack

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select the tube type for your buffer.
2. Upload your buffer volume CSV.
3. Set the DNA volume.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will transfer buffer to all wells in the output plate defined in the CSV file using the P300 single-channel pipette.
10. Robot will transfer each column of the DNA plate to each column of the output plate.


### Additional Notes
CSV Layout:

![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1483-aurora-diagnostics/csv_layout.png)

---

Buffer:
* Tube Rack: A1, B1, C1...
* Number of buffer tubes depends on how much buffer it requires to fill all of the wells defined in the CSV file

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
yIkoNMLW
1483

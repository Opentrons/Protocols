# Serial Dilution with CSV Input

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Serial Dilution

## Description
With this protocol, your robot can perform serial dilution on up to 40 samples. The number of dilutions and each buffer and sample volume are defined by a CSV input. See Additional Notes for more details on the required CSV layout. After the serial dilutions are completed, the robot will transfer each final dilution sample in duplicate to a new assay plate (bDNA plate) containing a specific amount of buffer.

---

You will need:
* P10 Multi-channel Pipette
* P300 Multi-channel Pipette
* 96-well Plates
* 12-row Trough
* 10 uL Tip Rack
* Opentrons 300 uL Tip Rack

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input the number of samples you are processing.
2. Upload your dilution CSV.
3. Input the starting column to fill samples in the bDNA plate.
4. Input the volume of buffer and samples to be transferred to the bDNA plate.
5. Download your protocol.
6. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".
10. Robot will distribute buffer from 12-row trough to the dilution plate(s).
11. Robot will serially dilute samples down the plate(s).
12. Robot will distribute buffer from 12-row trough to the bDNA plate.
13. Robot will transfer the last dilutions to the bDNA plate in duplicate.


### Additional Notes
Sample Plate(s) Setup:

![sample plate](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1488-atlas-genomics/sample_layout.png)

* Sample plates are in slot 1-5, you will only need all 5 plates if you have 40 samples and more than 5 dilutions (the max you can do is 11 dilutions per sample)
* Use a new plate if the next group of samples and their dilutions cannot fit on the rest of the plate

---

CSV Layout:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1488-atlas-genomics/csv_layout.png)

* This creates Example 1 layout from above
* Keep the headers
* Each row represents each dilution

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
TB9isL2R
1488

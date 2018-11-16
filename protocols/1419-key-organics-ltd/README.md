# Plate Normalization and Copying Using CSV Input

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Normalization

## Description
This protocol allows you to transfer and mix varying volumes of the same reagent from a [1-well trough](http://www.eandkscientific.com/8-Row-Reservoir-Deep-Well-Undivided-Pyramid-Bottom-290ml.html) into each individual well of up to two 96-well plates, using a P300 single-channel pipette. The volumes will be provided by user in the form of a CSV file. See Additional Notes for the CSV formatting requirements. After the normalization, the robot will "copy" all wells in the normalized plates to clean output plates, using a P300 multi-channel pipette. This transfer volume is the same across the plate, and will be defined by user in the customization field below.


### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your volume CSV for normalization.
2. Input your desired transfer volume for plate copying.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. The robot will transfer reagent to each well defined in your volume CSV, each transfer will use a new tip.
9. After all of the wells in the CSV have been normalized, the robot will transfer each column of the normalized plate(s) to a column of a clean output plate.

### Additional Notes
![format](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1419-key-organics-ltd/format.png)  
* Make sure to keep the header
* Plate: 1 or 2
* Well: A1 - H12 (no 0 between the alphabet and number)
* Volume: MIN = 30 uL (minimum volume of the P300 pipettes)
* Plate 1 is in slot 2, its output plate is in slot 3.
* (Optional) Plate 2 is in slot 5, its output plate is in slot 6.

Make sure you have this type of [trough](http://www.eandkscientific.com/8-Row-Reservoir-Deep-Well-Undivided-Pyramid-Bottom-290ml.html).

If you have any questions about this protocol, please email protocols@opentrons.com.

###### Internal
HBuPSVmr
1419

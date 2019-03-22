# DNA Normalization on Three Plates using CSV

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA Normalization

## Description
This protocol allows your robot to perform concentration normalization of DNA samples from up to 3 PCR plates to 3 clean new plates. Volumes to be transferred will be provided in the form of a CSV file. See Additional Notes below for more information on the required CSV format.

---

You will need:
* P50 Single-channel Pipette
* P300 Single-channel Pipette
* 1-well Disposable Reagent Reservoir
* [Biorad Hardshell 96-well PCR Plates](http://www.bio-rad.com/en-us/sku/hss9601-hard-shell-96-well-pcr-plates-high-profile-semi-skirted-clear-clear?ID=HSS9601)
* [SSIbio Semi-skirted 96-well PCR Plates](http://www.ssibio.com/pcr/ultraflux-pcr-plates/semi-skirted-pcr-plates/3450-00)
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your volume CSV.
2. Specify whether or not you would like to robot to pause after transferring the diluent so you could spin the plate down before transferring the samples.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will transfer diluent from reagent reservoir to each well specified in the volume CSV.
9. Depending on your specification, the robot will or will not pause until you resume the protocol.
10. Robot will transfer sample to each specified well in the volume CSV.


### Additional Notes
CSV Layout:

![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1532-agriculture-and-agri-food-canada/layout.png)

* Keep the headers
* Destination and Sample_ID format: Plate(slot number)-(well name)
* Diluent volume (uL)
* DNA volume (uL)

---

Plate Types:
* Biorad Hardshell Plates (Sample Plates): slot 1, 4, 7
* SSIbio Semi-skirted Plates (Output Plates): slot 2, 5, 8

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
5Zd5W9l7
1532

# DNA Normalization with CSV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* DNA Quantification


## Description
This protocol normalizes DNA concentration on a secondary plate dependent on a CSV file. The CSV file must be uploaded (below) and should be formatted as such:

`Well` | `DNA Concentration (ng/μl)`

The CSV should not include headers. Based on the values in the CSV and the desired final volume/concentration (input below), the robot will transfer the corresponding DNA (from sample plate) and water (from conical tube) to the final plate to create the desired concentration at the desired volume.

Note: If the mathematically determined volume of DNA to be transferred to the final plate is larger than the desired volume, the robot will just transfer the desired volume from the sample plate to the final plate without the addition of water (this case occurs if the initial concentration is lower than the final desired concentration).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Opentrons P50 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [Opentrons P10 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [Opentrons 50μl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 10μl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 4-in-1 Tube Rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 15mL Conical Tube
* [Bio-Rad 96-Well Plate, 200μl](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr?category=wellPlate)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Bio-Rad Plate](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr?category=wellPlate) (with DNA samples)

Slot 2: [Bio-Rad Plate](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr?category=wellPlate) (clean and empty)

Slot 3: [Opentrons 4-in-1 Tube Rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* A1: 15mL Conical Tube filled with water

Slot 4: [Opentrons 50μl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 5: [Opentrons 10μl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Upload CSV and input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
7d113b

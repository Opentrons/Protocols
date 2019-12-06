# Cherrypicking with Source and Destination

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Consolidation


## Description
Cherrypicking, or hit-picking, is a key component of many workflows from high-throughput screening to microbial transfections. With this protocol, you have the ability to choose from a variety of labware, including the **Starlab Deepwell Plate** (see note below) and Eppendorf Tubes (1.5mL/2mL) in the Opentrons Tube Rack. Using a CSV (.csv) that is uploaded below, you can specify the volume to be transferred between which source well and which destination well.

The CSV should be formatted like so:

`Source Well` | `Volume` | `Destination Well`

**Note about Labware**: The Starlab Deepwell Plate falls outside our [Standard Labware Library](https://labware.opentrons.com/). In order to use this piece of labware in your protocol, please upload the JSON file found in the `labware` folder that accompanies the protocol download, to the Opentrons App, before uploading the protocol. For more information, please see [this article](https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols).

**Note about CSV**: The first column is dedicated to the header of the CSV; thus, the first row of data should occupy cells 'A2', 'B2', and 'C2' in the document.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.15.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes) and corresponding [Tips](https://shop.opentrons.com/collections/opentrons-tips)
* Source Labware (see below for more information)
* Destination Labware (see below for more information)


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

For this protocol, you will load your source labware in Slot 2 and your destination labware in Slot 3. The tip racks should be loaded in Slots 1, 4, 7, and 10 (as needed).

Using the customization fields below, set up your protocol.
* Volumes CSV: Upload your properly formatted CSV here. This will dictate all of the transfers in the protocol.
* Pipette Model: Select which pipette you will use for this protocol.
* Pipette Mount: Specify which mount your single-channel pipette is on (left or right).
* Source Labware Type: Select which (destination) labware you will use for this protocol.
* Destination Labware Type: Select which (destination) labware you will use for this protocol.
* Tip Usage Strategy: Select whether you would like to use the same tip or a new tip for each transfer.


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Upload CSV and input your protocol parameters.
2. Download your protocol.
3a. If using the Starlab plate, upload the JSON file to the [OT App](https://opentrons.com/ot-app).
3b. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Applications Engineering Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
7a3e4b

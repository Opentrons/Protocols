# Custom Cherrypicking from CSV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
     * Cherrypicking

## Description

This protocol uses a p300 single channel pipette (starting tip specified as a parameter at the time of protocol download) to transfer custom volumes of DNA from a source plate to a destination plate (volume, deck slots and well locations specified by user in a csv file uploaded at the time of protocol download).

Links:
* [example input csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5a2a35/Cherrypicking+CSV.csv)

This protocol was developed to transfer custom volumes of DNA from one of possibly several source plates to one of possibly several destination plates according to volumes, deck slot numbers, and well locations in the uploaded csv file. The user selects the starting tip box and tip as a parameter value (using the parameter settings below) at the time of protocol download.

## Protocol Steps

Set up: Up to a total of 6 source and destination plates (number should be equal to plate_count parameter value set below at the time of protocol download) should be placed in deck slots 1-6 (adhering to deck slot fill order of 1, 2, 3, 4, 5, 6), three boxes of Opentrons 200 ul filter tips in deck slots 7-9, deck slots 10 and 11 empty.

The OT-2 will perform the following steps:
1. User selects starting tip location.
2. Tip picks up.
3. Aspirate DNA volume based on CSV.
4. Aspirate air gap of 5uL.
5. Transfer DNA to destination location/well based on CSV.
6. Dispense full amount toward the bottom of the well.
7. Discard tip in trash.
8. Repeat steps 2-7 until all lines in CSV are completed.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.19.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons Single-Channel p20 and Single-Channel p300 Pipettes](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons Tips for the p20 and p300 Pipettes](https://shop.opentrons.com/collections/opentrons-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5a2a35/5a2a35_layout.png)

* Opentrons 200ul filter tips (Deck Slots 7, 8, and 9)
* Selected Plate Labware for Source and Destination Plates (Deck Slots 1-6)

![input csv data and file format](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5a2a35/CherrypickingCSV.png)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. User the protocol parameter settings on this page to choose the starting tip, the number of plates on deck, and upload the input csv file (containing info about source and destination plate deck slots, well locations and transfer volumes-see example for data and file format).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5a2a35

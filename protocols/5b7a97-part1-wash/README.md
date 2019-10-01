# MagMAX Part 1/3: Customizable Processing Plate Filling

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Filling


## Description
This protocol fills plates with either wash solution 1, wash solution 2, or the elution buffer as outlined in the [MagMax protocol](https://www.thermofisher.com/document-connect/document-connect.html?url=https%3A%2F%2Fassets.thermofisher.com%2FTFS-Assets%2FLSG%2Fmanuals%2FMAN0015944_MagMAXCORE_NA_Kit_UG.pdf&title=VXNlciBHdWlkZTogTWFnTUFYIENPUkUgTnVjbGVpYyBBY2lkIFB1cmlmaWNhdGlvbiBLaXQ=). The user can specify the number of plates they'd like to fill (1-6) and whether to create full plates or half plates. This protocol is part 1 of a 3-part protocol.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P300 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Nalgene 300ml Reservoir](https://www.thermofisher.com/order/catalog/product/1200-1300)
* Sample Plates: [KingFisher 96-Well Plate](https://www.thermofisher.com/order/catalog/product/95040450) or [KingFisher DeepWell Plate](https://www.thermofisher.com/order/catalog/product/95040450)


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: Sample Plate

Slot 2: Sample Plate (optional)

Slot 3: Sample Plate (optional)

Slot 4: Sample Plate (optional)

Slot 5: Sample Plate (optional)

Slot 6: Sample Plate (optional)

Slot 7: [300ul Opentrons tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 8: Nalgene Reservoir (filled with either Wash Solution 1, Wash Solution 2, or the Elution Buffer)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters (number of plates; half- or full-plates).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5b7a97

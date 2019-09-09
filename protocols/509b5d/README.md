# Kylt RNA/DNA Purification HTP

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
This protocol performs RNA/DNA purification with the OT-2 according the Kylt protocol which can be found [here](https://www.kylt.eu/templates/images/products/436_1_pdf/Kylt_Handbuch-RNA-DNA-Purification_HTP_Rev03.pdf).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P50 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P300 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Ritter 2.5 ml Square-Deep-Well Plate](https://www.ritter-medical.de/en/products/riplate-square-wells/)
* [U-Bottom 96-well Microtiter Plate](https://labware.opentrons.com/corning_96_wellplate_360ul_flat/)
* [4 Column Reservoir](https://www.agilent.com/store/en_US/LCat-SubCat1ECS_112089/Reservoirs)
* [12 Column Reservoir](https://www.agilent.com/store/en_US/LCat-SubCat1ECS_112089/Reservoirs)
* [1 Column Reservoir](https://www.agilent.com/store/en_US/LCat-SubCat1ECS_112089/Reservoirs)

* [Kylt Protocol Reagents](https://www.kylt.eu/templates/images/products/436_1_pdf/Kylt_Handbuch-RNA-DNA-Purification_HTP_Rev03.pdf)
	* Lysis Solution
	* Proteinase K
	* Magnetic Beads
	* Binding Solution
	* Wash Solution
	* Elution Buffer
	* 80% non-denatured Ethanol



---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: 96-well Microtiter Plate, clean and empty

Slot 3: [1 Column Reservoir](https://www.agilent.com/store/en_US/LCat-SubCat1ECS_112089/Reservoirs), empty (for waste)

Slot 4: [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck) loaded with [Ritter 2.5 ml Square-Deep-Well Plate](https://www.ritter-medical.de/en/products/riplate-square-wells/) filled with samples

Slot 5: [12 Column Reservoir](https://www.agilent.com/store/en_US/LCat-SubCat1ECS_112089/Reservoirs)
	* Column 1: Proeinase K
	* Column 3: Lysis Solution
	* Column 5: Magnetic Beads
	* Column 7: Elution

Slot 6: [4 Column Reservoir](https://www.agilent.com/store/en_US/LCat-SubCat1ECS_112089/Reservoirs)
	* Column 1: Binding Solution
	* Column 2: Wash Solution
	* Column 3: (OPTIONAL) Wash Solution
	* Column 4: 80% Ethanol

Slot 7: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 8: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 9: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your pipette parameters, number of samples, and add optional second wash step (note: if doing the optional 2nd wash, make sure that wash solution is loaded in Columns 2 AND 3 of the 4 Column Reservoir).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
This protocol does not use a heated-shaker plate during incubation.

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
509b5d

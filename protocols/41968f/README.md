# Magbead Based Peptide Purification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
This protocol performs protein purification using magnetic Ni-charged beads according to the protocol which can be found [here](https://www.genscript.com/kit/L00295-Ni_charged_MagBeads.html).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P300 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Square-Deep-Well Plate, 2 mL](https://www.capitolscientific.com/Whatman-7701-5200-UNIPLATE-96-Well-x-2mL-Assay-Collection-Analysis-MicroPlate-Natural-Polyprop)
* [96-well Microtiter Plate](https://shop.gbo.com/en/usa/products/bioscience/microplates/96-well-microplates/)
* [4 Column Reservoir](https://www.sigmaaldrich.com/catalog/product/sigma/br701454?lang=en&region=US)

* [Protocol Reagents](https://www.genscript.com/kit/L00295-Ni_charged_MagBeads.html)
	* Wash Solution
	* Elution Buffer



---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [96-well Microtiter Plate](https://shop.gbo.com/en/usa/products/bioscience/microplates/96-well-microplates/), clean and empty

Slot 3: [4 Column Reservoir](https://www.sigmaaldrich.com/catalog/product/sigma/br701454?lang=en&region=US), empty (for waste)

Slot 4: [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck) loaded with [Square-Deep-Well Plate, 2 mL](https://www.capitolscientific.com/Whatman-7701-5200-UNIPLATE-96-Well-x-2mL-Assay-Collection-Analysis-MicroPlate-Natural-Polyprop), filled with 30 uL magnetic bead slurry

Slot 5: [96-well Microtiter Plate](https://shop.gbo.com/en/usa/products/bioscience/microplates/96-well-microplates/), filled with 300 uL cell-free lysate, 96 different samples (sample plate)

Slot 6: [4 Column Reservoir](https://www.sigmaaldrich.com/catalog/product/sigma/br701454?lang=en&region=US)
	* Column 1: Wash Solution
	* Column 2: Wash Solution
	* Column 3: Wash Solution
	* Column 4: Elution Buffer

Slot 7: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 8: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 9: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 10: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters: pipette mount (left or right), rate of aspiration for supernatant (in uL/sec. Should be between 5 and 150), and time for magbead separation (in seconds).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
41968f

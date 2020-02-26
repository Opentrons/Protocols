# Bp Genomics RNA Extraction

### Author
[Opentrons](https://opentrons.com/)

### Partner
[BP Genomics](https://bpgenomics.com/)

## Categories
* Sample Prep
	* RNA Extraction


## Description
**This protocol is currently being tested and is subject to change**

This protocol automates the pureBASE RNA protocol by BP Genomics.

Additionally, it adds the 4ul of internal extraction control RNA as described in the 2019-nCoV Detection Assay protocol.


---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase consumables, labware, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.15.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons P20 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P1000 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [NEST 96-Well PCR Plate](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt)
* [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/reservoirs/products/nest-12-well-reservoir-15-ml)
* NEST Deep Well Plate, 1mL
* [NEST 1-Well Reservoir, 195mL](https://labware.opentrons.com/nest_1_reservoir_195ml?category=reservoir)



---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

*May need to change pending revisions*

Slot 1: [NEST 96-Well PCR Plate](https://shop.opentrons.com/collections/lab-plates/products/nest-0-1-ml-96-well-pcr-plate-full-skirt) (for elutes)

Slot 3: Opentrons 20ul Filter Tips

Slot 4: MagDeck, with Deep Well Plate containing 400ul of sample

Slot 5: 12-Well Reservoir

Slot 6: Opentrons 1000ul Filter Tips

Slot 8: Reservoir for Liquid Waste






__Using the customizations fields, below set up your protocol.__
* **Number of Samples**: Specify the number of samples you'd like to run.
* **P20 Single Mount**: Specify which mount (left or right) the P20 Single is attached to.
* **P1000 Single Mount**: Specify which mount (left or right) the P1000 Single is attached to.





### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
bpg-rna-extraction

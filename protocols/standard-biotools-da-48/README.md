# Standard BioTools Dynamic Array 48.48: Load 4 uL


### Author
[Standard BioTools](https://www.standardbio.com/)

### Partner
[Opentrons](https://opentrons.com/)


## Categories
* Sample Prep
	* Standard BioTools


## Description
![Standard BioTools Logo](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/standard-biotools/standard-bio-logo-200-TM.jpg)
</br>
This protocol transfers 4 µL of samples and assays from 96-well plates to the Standard BioTools 48.48 IFC (Integrated Fluidic Circuit)</br>
![Standard BioTools 48](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/standard-biotools/Opentrons_IFC_48.jpg)
</br>
**Preparation**:</br>
Before beginning the protocol on the OT-2, perform the following preparation steps:
1. Prepare the Samples, the Assays, and the IFC Referring as described in one of the following workflows from the Standard BioTools X9 User Guide:
- Gene Expression Using the 48.48 IFC-X with TaqMan Assays
2. Prepare a Sample Plate by transferring 6 µL of sample to 48 wells of a 96-well plate
3. Prepare an Assay Plate by transferring 6 µL of assay to 48 wells of a 96-well plate
4. *NOTE*: All wells (indicated below in blue) must have liquid
5. Centrifuge the Sample and Assay plates to ensure liquids are at the bottom of the wells
6. Prepare the 48.48 IFC:
- Add control line fluid to the accumulators according to the workflow selected in step 1 (Indicated above by red arrows)
- Remove the protective film from the bottom of the IFC


### Labware
* Standard BioTools 48.48 Dynamic Array IFC
* [Opentrons 96 Well Aluminum Block](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [NEST 96-Well PCR Plate, 100µL](https://shop.opentrons.com/nest-0-1-ml-96-well-pcr-plate-full-skirt/)
* [Opentrons 20µL Filter Tips](https://shop.opentrons.com/opentrons-20ul-filter-tips/)


### Pipettes
* [Opentrons P20 8-Channel Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/standard-biotools/Opentrons+Protocols+Figs_48.48+Layout.jpg)


### Protocol Steps
1. Transfer assays to left side of IFC
2. Transfer samples to right side of IFC
</br>
*NOTE*: Mapping from the sample / assay plates to the IFC matches the mapping defined by the workflow selected in Preparation: Step 1



### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `labware` > `Import`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit "Run".


### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).


###### Internal
standard-biotools-da-48

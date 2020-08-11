# COVID-19 RNA Extraction

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* COVID-19
    * RNA Extraction

## Description
This is a flexible protocol accommodating a wide range of commercial RNA extraction workflows for COVID-19 sample processing. The protocol is broken down into 5 main parts:
* binding buffer addition to samples
* bead wash 3x using magnetic module
* final elution to chilled PCR plate

Lysed samples should be loaded on the magnetic module in a NEST 96-deepwell plate. For reagent layout in the 2 12-channel reservoirs used in this protocol, please see "Setup" below

This protocol allows your robot to create a master mix solution using any reagents stored in a 2 mL Eppendorf tube rack or a 2 mL screwcap tube rack. The master mix will be created in well A1 of the trough. The ingredient information will be provided as a CSV file. See Additional Notes for more details.

---

![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)  

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons magnetic module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons temperature module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [NEST 12 Well Reservoir 15 mL](https://labware.opentrons.com/nest_12_reservoir_15ml)
* [NEST 1 Well Reservoir 195 mL](https://labware.opentrons.com/nest_1_reservoir_195ml)
* [NEST 96 Well Plate 100 µL PCR Full Skirt](https://labware.opentrons.com/nest_96_wellplate_100ul_pcr_full_skirt)
* [NEST 96 Deepwell Plate 2mL](https://labware.opentrons.com/nest_96_wellplate_2ml_deep)
* [Opentrons 96 Filter Tip Rack 200 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-200ul-filter-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

* Reservoir 1: slot 5
* Reservoir 2: slot 2
![reservoirs](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/covid-19-station-b/reagent_layout.png)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Select your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
covid-19-rna-extraction

# Z'LYTE Kinase Assay Kits Part 1/2: Kinase Reaction

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Assay

## Description
Links: [Part 1](./1376-arold-lab-kaust-part1) [Part 2](1376-arold-lab-kaust-part2)
This protocol requires a P10 single channel pipette. User will define the both the location of the reagents to be distributed as well as the destination well on the target 96-well plate by uploading CSVs. See Additional Notes for more information on the CSV formats.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [TempDeck](https://shop.opentrons.com/products/tempdeck)

### Reagents
* [Z'-LYTE Kinase Assay Kits](https://www.thermofisher.com/ch/en/home/industrial/pharma-biopharma/drug-discovery-development/target-and-lead-identification-and-validation/kinasebiology/kinase-activity-assays/z-lyte.html)

## Process
1. Input the temperature that the TempDeck should maintain throughout the protocol.
2. Upload your Reagent Location CSV.
3. Upload your Assay Setup CSV.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. TempDeck will heat up or cool down to your desired temperature.
10. Robot will transfer the reagents to the target plate based on the volumes defined in the Assay Setup CSV using the single-channel pipette.

### Additional Notes
![CSV setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1376-arold-lab-kaust/csv_part_1.png)

Assay Setup CSV
* First column *must* be the destination wells.
* The header of the columns from second column on must match the reagent names in the Reagent Location CSV.
* Each value is the volume of the reagent of that column to be transferred to the target well in column 1 of that row.
* Order of the columns is the order of which the reagents to be transferred in the protocol, i.e. in the example above, water will be distributed into well A1, B2, C2, D2, and then substrate A+ will be transferred to well A1, and so on...

Reagent Location CSV
* First column *must* be the name of the reagents. They must match the headers of the assay setup.
* Second column *must* be the name of the container, see a list of pre-defined container below.
* Third column *must* be slot on the deck, the number has to be 3-10.

Pre-defined Container
* opentrons-tuberack-15_50ml
* opentrons-tuberack-15ml
* opentrons-tuberack-2ml-eppendorf
* opentrons-tuberack-2ml-screwcap
* opentrons-tuberack-50ml
* trough-12row
* 96-deep-well
* If you would like to use other containers, email protocols@opentrons.com.

###### Internal
WOEADNei
1376

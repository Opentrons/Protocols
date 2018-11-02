# Z'LYTE Kinase Assay Kits Part 2/2: Kinase Reaction

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Assay

## Description
Links: [Part 1](./1376-arold-lab-kaust-part1) [Part 2](1376-arold-lab-kaust-part2)  
This protocol requires a P10 single-channel and a P10 multi-channel pipette. User will need to upload 3 CSVs in this protocol and define an incubation time between the Development Reaction and the Stop Step. User will define the both the location of the reagents to be distributed as the Reagent Location CSV. The destination wells of the Development agents on the target 96-well plate will be defined in the Development Agent CSV. The destination columns of the Stop Reagent on the plate will be defined in the Stop Reagent CSV. See Additional Notes for more information on the CSV formats.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [TempDeck](https://shop.opentrons.com/products/tempdeck)

### Reagents
* [Z'-LYTE Kinase Assay Kits](https://www.thermofisher.com/ch/en/home/industrial/pharma-biopharma/drug-discovery-development/target-and-lead-identification-and-validation/kinasebiology/kinase-activity-assays/z-lyte.html)

## Process
1. Input the temperature that the TempDeck should maintain throughout the protocol.
2. Upload your Reagent Location CSV.
3. Upload your Development Agent CSV.
4. Input the desired incubation (minutes).
5. Upload your Stop Reagent CSV.
6. Download your protocol.
7. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
8. Set up your deck according to the deck map.
9. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
10. Hit "Run".
11. TempDeck will heat up or cool down to your desired temperature.
12. Robot will transfer the reagents to the target plate based on the volumes defined in the Development Agent CSV using the single-channel pipette.
13. Robot will pause and incubate the target plate.
14. Robot will transfer the reagents to the target plate based on the volumes defined in the Stop Reagent CSV using the multi-channel pipette.

### Additional Notes
![CSV setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1376-arold-lab-kaust/csv_part_2.png)

Development Agent CSV
* First column *must* be the destination wells.
* The header of the columns from second column on must match the reagent names in the Reagent Location CSV.
* Each value is the volume of the reagent of that column to be transferred to the target well in column 1 of that row.
* Order of the columns is the order of which the reagents to be transferred in the protocol, i.e. in the example above, development 1 will be distributed into well C2, D2, G2, and H2 and then Development 2 will be transferred to well A2, B2, E2, and F2.

Stop Reagent CSV
* First column *must* be the destination columns, i.e. in the example above, stop reagent will be transferred to the entire column 2 of the target plate using the multi-channel pipette.

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

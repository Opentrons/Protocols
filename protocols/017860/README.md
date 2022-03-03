# Protocol Title (should match metadata of .py file)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* CSV Transfer

## Description
This is an OT-2 compatible protocol that first transfers media and up to 35 different antibiotics plus barcoding dye to the wells of up to six 96 well plates based on an input CSV file. If there are more entries once the plate(s) have been filled the user is asked to replace the plates with fresh ones and the process continues until all rows of the input file have been processed.

The protocol takes its input
* `input .csv file`: Here, you should upload a .csv file formatted in the following way, being sure to include the header line:

The first column is an identifier and is discarded by the protocol, the 2nd column is the M9 media stored in 3 50 mL tubes on slot 8. The remaining columns up to n-1 are antibiotics stored on 15 mL tuberack 1 and 2 (see below). The nth tube is barcoding dye.
```
,M9,antibiotic 1, antibiotic 2, ... , antibiotic n, barcoding dye
99999,50,0,0,...,0,50
100,90,10,0,...,0,0
```
* `20 uL pipette tips`: Brand of pipette tips either Opentrons or BrandTech 20 uL tips
* `300 uL pipette tips`:  Brand of pipette tips either Opentrons or BrandTech 300 uL tips
* `Number of plates`: Number of 96 well plates on the deck per run, may range from one to six

---

### Labware
* [Opentrons 20 uL tipracks](https://shop.opentrons.com/opentrons-20-l-tips-160-racks-800-refills/)
* [300 uL tipracks](https://shop.opentrons.com/opentrons-300ul-tips-1000-refills/)
* [BrandTech 20 uL tipracks](https://brandtech.com/product/standard-tips/)
* [BrandTech 300 uL tipracks](https://brandtech.com/product/standard-tips/)
* [Nunc 400 µL 96 well plate](https://www.thermofisher.com/us/en/home/life-science/cell-culture/cell-culture-plastics/nunc-plate-selection-guide.html#!/n_format:96)
* [Opentrons tuberacks](https://shop.opentrons.com/4-in-1-tube-rack-set/)
* [Opentrons tubes](https://shop.opentrons.com/consumables/)
* [Falcon tubes](https://ecatalog.corning.com/life-sciences/b2c/US/en/Liquid-Handling/Tubes%2C-Liquid-Handling/Centrifuge-Tubes/Falcon%C2%AE-Conical-Centrifuge-Tubes/p/falconConicalTubes)

### Pipettes
* [P20 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P300 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

### Reagents
* M9 media in 50 mL tubes on slot 8
* Antibiotics in 15 mL tuberack on slot 9 and 7 and the 15 mL tubes on slot 8.

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/017860/deck.jpg)
Slots:
1. Nunc 96 well plate 1
2. Nunc 96 well plate 2 (optional)
3. Nunc 96 well plate 3 (optional)
4. Nunc 96 well plate 4 (optional)
5. Nunc 96 well plate 5 (optional)
6. Nunc 96 well plate 6 (optional)
7. Tuberack with 15 mL tubes antibiotic tuberack #2
8. Tuberack 4x50 mL/6x15 mL tubes - Media and antibiotics #3
9. Tuberack with 15 mL tubes antibiotic tuberack #1
10. 20 µl tiprack
11. 300 µL tiprack


### Reagent Setup
* This section can contain finer detail and images describing reagent volumes and positioning in their respective labware. Examples:
* Reservoir 1: slot 5
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res1_v2.png)
* Reservoir 2: slot 2  
![reservoir 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res2.png)

---

### Protocol Steps
1. This section should consist of a numerical outline of the protocol steps, somewhat analogous to the steps outlined by the user in their custom protocol submission.
2. example step: Samples are transferred from the source tuberacks on slots 1-2 to the PCR plate on slot 3, down columns and then across rows.
3. example step: Waste is removed from each sample on the magnetic module, ensuring the bead pellets are not contacted by the pipette tips.

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
protocol-hex-code

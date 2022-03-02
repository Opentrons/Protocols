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
```
source,dest,vol
A1,B1,4
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

### Pipettes
* [P20 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P300 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

### Reagents
* M9 media
* Antibiotics

---

### Deck Setup
* If the deck layout of a particular protocol is more or less static, it is often helpful to attach a preview of the deck layout, most descriptively generated with Labware Creator. Example:
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

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

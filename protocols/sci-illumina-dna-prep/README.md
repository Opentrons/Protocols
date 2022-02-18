# Illumina DNA Prep - Opentrons v3
### Author
[Opentrons](https://opentrons.com/)

### Partner
[Illumina](https://www.illumina.com/)

## Categories
* NGS Library Prep
  * Illumina DNA Prep

## Description
This protocol automates the [Illumina DNA prep protocol](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/illumina_prep/illumina-dna-prep-reference-guide-1000000025416-09.pdf). Illumina DNA prep offers a fast, integrated workflow for a wide range of applications, from human whole-genome sequencing to amplicons, plasmids, and microbial species

In the protocol there is a setting for the number of samples which may be 8, 16 or 24 (i.e. 8 samples per column, up to 3 columns).  Samples are prepared as below, with 30ul of 100ng of sample DNA.  See the Illumina DNA Prep protocol for more information about sample input requirements.

![Sample input and output columns](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-illumina-dna-prep/v3/samples_output.jpg)

![Sample columns](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-illumina-dna-prep/v3/sample_setup.jpg)

**Plate Moving**
The Protocol requires manually transferring the sample plate between the Thermocycler and Magnet 3 times.  It starts on the Thermocycler and needs to be moved to the Magnet for the post-Tagmentation washes, and then moved to the Thermocycler for PCR and then back to the Magnet for the post-PCR cleanup.  In the script the two positions are handled as sample_plate_mag and sample_plate_thermo; during calibration use an empty plate of the same labware as the sample plate on the magnet position to allow calibration.


Explanation of parameters below:
* `Number of samples`: 8 (column 1), 16 (column 1, 3), or 24 (column 1, 3, 5) samples (see above).

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Thermocycler Module](https://shop.opentrons.com/collections/hardware-modules/products/thermocycler-module)

### Labware
* [Nest 96 well plate full skirt 100 µL](https://shop.opentrons.com/nest-0-1-ml-96-well-pcr-plate-full-skirt/)
* [NEST 2 mL 96-Well Deep Well Plate](https://shop.opentrons.com/nest-2-ml-96-well-deep-well-plate-v-bottom/)
* [NEST 12-Well Reservoirs, 15 mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* Optional: [Eppendorf 96 well plate full skirt](https://online-shop.eppendorf.us/US-en/Laboratory-Consumables-44512/Plates-44516/Eppendorf-twin.tec-PCR-Plates-PF-8180.html?_gl=1*1gk1ehp*#Accessory)
* [Opentrons aluminum block set](https://shop.opentrons.com/aluminum-block-set/)

### Pipettes
* [P300 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P20 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

**Tips**
* [Opentrons 20 µL filter tiprack](https://shop.opentrons.com/opentrons-20ul-filter-tips/)
* [Opentrons 200 µL filter tiprack](https://shop.opentrons.com/opentrons-200ul-filter-tips/)

### Reagents
* [Illumina DNA Prep](https://www.illumina.com/products/by-type/sequencing-kits/library-prep-kits/nextera-dna-flex.html)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-illumina-dna-prep/v3/deck.jpg)

Slots:
1. Sample plate: Magnetic module with  Nest 96 well plate full skirt (or Eppendorf 96 well plate full skirt) 100 µL wells
2. Reagent plate 1: NEST 12 well 15 mL reservoir (or NEST 96 deep-well plate 2 mL when reusing tips). See Reagent Setup section for information about the location of the reagents
3. Reagent plate 2: Temperature module with Bio-rad 200 µL plate on aluminum block. See Reagent Setup section for information about the location of the reagents
4. 20 µL filter tiprack
5. 200 µL filter tiprack
6. 200 µL filter tiprack
7. Sample plate: Thermocycler module with NEST 96 well plate full skirt 100 µL
8. Empty
9. 200 µL filter tiprack
10. Sample plate: Thermocycler module with NEST 96 well plate full skirt (or Eppendorf 96 well plate full skirt) 100 µL
11. Empty

### Reagent Setup
* Reagent plate 1, slot 2:
![Reagent plate 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-illumina-dna-prep/v3/reagent_plate1.jpg)
* Reservoir 2, slot 3:
![Reagent plate 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-illumina-dna-prep/v3/reagent_plate2.jpg)

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
illumina-dna-prep

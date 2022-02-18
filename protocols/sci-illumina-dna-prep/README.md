# Illumina DNA Prep
### Author
[Opentrons](https://opentrons.com/)

### Partner
[Illumina](https://www.illumina.com/)

## Categories
* NGS Library Prep
  * Illumina DNA Prep

## Description
This protocol automates the [Illumina DNA prep protocol](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/illumina_prep/illumina-dna-prep-reference-guide-1000000025416-09.pdf). Illumina DNA prep offers a fast, integrated workflow for a wide range of applications, from human whole-genome sequencing to amplicons, plasmids, and microbial species

In the protocol there is a setting definition for the number of samples (SAMPLES = 8x, 16x, or 24x).  Samples are prepared as below, with 30ul of 100ng of sample DNA.  See the Illumina DNA Prep protocol for more information about sample input requirements.

Example: This is a flexible protocol accommodating a wide range of commercial RNA extraction workflows for COVID-19 sample processing. The protocol is broken down into 5 main parts:
* binding buffer addition to samples
* bead wash 3x using magnetic module
* final elution to chilled PCR plate

Subsequent paragraphs can give some more insight into the details of the protocol, but a step-by-step description should be included in the 'Protocol Steps' section below.

Example: For sample traceability and consistency, samples are mapped directly from the magnetic extraction plate (magnetic module, slot 4) to the elution PCR plate (temperature module, slot 1). Magnetic extraction plate well A1 is transferred to elution PCR plate A1, extraction plate well B1 to elution plate B1, ..., D2 to D2, etc.

Results of the Opentrons Science team's internal testing of this protocol on the OT-2 are shown below:  
![results](link_to_results.png)

Explanation of parameters below:
* `Number of samples`: 8 (column 1), 16 (column 1, 3), or 24 (column 1, 3, 5) samples

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Thermocycler Module](https://shop.opentrons.com/collections/hardware-modules/products/thermocycler-module)
* [HEPA Module](https://shop.opentrons.com/collections/hardware-modules/products/hepa-module)

### Labware
* [Labware name](link to labware on shop.opentrons.com when applicable)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

### Pipettes
* [Pipette name](link to pipette on shop.opentrons.com)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

### Reagents
* [kit name when applicable](link to kit)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

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

# Protocol Title (should match metadata of .py file)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Pooling

## Description
This section of the README (especially the first paragraph) should grip a prospective user with the overarching purpose/flow of the protocol, but should not include fine details of the protocol steps themselves.

Example: This is a flexible protocol accommodating a wide range of commercial RNA extraction workflows for COVID-19 sample processing. The protocol is broken down into 5 main parts:
* binding buffer addition to samples
* bead wash 3x using magnetic module
* final elution to chilled PCR plate

Subsequent paragraphs can give some more insight into the details of the protocol, but a step-by-step description should be included in the 'Protocol Steps' section below.

Example: For sample traceability and consistency, samples are mapped directly from the magnetic extraction plate (magnetic module, slot 4) to the elution PCR plate (temperature module, slot 1). Magnetic extraction plate well A1 is transferred to elution PCR plate A1, extraction plate well B1 to elution plate B1, ..., D2 to D2, etc.

Results of the Opentrons Science team's internal testing of this protocol on the OT-2 are shown below:  
![results](link_to_results.png)

Explanation of complex parameters below:
* `input .csv file`: Here, you should upload a .csv file formatted in the following way, being sure to include the header line:
```
source,dest,vol
A1,B1,4
```

---

### Modules
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck) - Not used in protocol but loaded so module can remain on the deck

### Labware
* [Labware name](link to labware on shop.opentrons.com when applicable)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

### Pipettes
* [Pipette name](link to pipette on shop.opentrons.com)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

### Reagent Setup
* Reservoir 1: slot 5
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res1_v2.png)
* Reservoir 2: slot 2  
![reservoir 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res2.png)

---

### Protocol Steps
1. Use a single channel pipettor and a new tip each time, transfer 2-35 uL from the 96 well PCR plate to a single 2 mL snap tube
2. Repeat across the entire plate according to the .csv file

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
0dda91

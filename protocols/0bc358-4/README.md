# Protocol Title (#1 Calibrator / Quality Control Working Stock Prep)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Standard Curve

## Description
This protocol will create Calibrator Working Stocks (WS1, WS2, WS3, WS4) and Quality Control working stock (QC1, QC2, QC3, QC4) by diluting analytes in methanol. 

---

### Labware
* [OT-2 Filter Tips, 200µL (999-00081))](https://shop.opentrons.com/opentrons-200ul-filter-tips/)
* [OT-2 Filter Tips, 1000µL (999-00082)](https://shop.opentrons.com/opentrons-1000ul-filter-tips-1000-racks/)
* [Verex Vials in Custom 54-Position Rack](https://www.phenomenex.com/part?partNo=AR0-9921-13)
* [11-Position Block for 28 mm Scintillation Flat Bottom Vials](https://chemglass.com/blocks-for-centrifugal-vacuum-evaporators-optichem?sku=OP-6600-11)


### Pipettes
* [P300 GEN2 Single Channel Pipette](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P1000 GEN2 Single Channel Pipette](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

### Reagents
* [Analytes](various)
* [Methanol](link to product not available)

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
1. MeOH is added to the WS1 (A1) and QC1 (C1) scintillation vials in tuberack on slot 3.
2. Analytes are transferred from the source tuberacks on slot 2 to the WS1 and QC1 scintillation vials.
3. MeOH is added to the WS2 (A2) and QC2 (C2) scintillation vials in tuberack on slot 3.
4. Analytes are transferred from the source tuberacks on slot 5 to the WS2 and QC2 scintillation vials.
5. MeOH is added to the WS3 (A3) and QC3 (C3) scintillation vials in tuberack on slot 3
6. Analytes are transferred from the source tuberacks on slot 8 to the WS3 and QC3 scintillation vials (note protocol will pause to replace/refill analyte vials in D3 and D4 of the source tuberack between aspiration steps).
7. MeOH is added to the WS4 (A4) and QC4 (C4) scintillation vials in tuberack on slot 3
8. Analytes are transferred from the source tuberacks on slot 11 to the WS4 and QC4 scintillation vials with a pause before each analyte to remove caps.

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
0bc358

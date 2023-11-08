# Protocol Title (#4 Making Calibrator Curve using 20 mL Scintillation Vial)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Standard Curve

## Description
This protocol will create Calibrator Curves from Working Stocks (WS1, WS2, WS3, WS4) diluting 275 µL of each Working Stock in 4.4 mL of Blank Urine. 

---

### Labware
* [OT-2 Filter Tips, 1000µL (999-00082)](https://shop.opentrons.com/opentrons-1000ul-filter-tips-1000-racks/)
* [12 Well Aluminum Vial Tray, for 28mm Flat bottom Vials](https://www.analytical-sales.com/product/12-well-aluminum-vial-tray-27-8mm-well-diameter/)
* [Neptune Tiprack Base 1 Reservoir 300 mL](Link not available) 

### Pipettes
* [P1000 GEN2 Single Channel Pipette](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

### Reagents
* [Blank Urine](various)
* [Calibrator Working Stocks C10-C2](link to product not available)

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
1. 4400 µL of Blank Urine is added to the scintillation vials in positions A1-A4, B1-B4 and C1 in tuberack on slot 11.
2. 275 ul of each C10 WS-1, WS-2, WS-3 and WS-4 in positions A1-A4 of the tuberack on slot 7 is then transferred to the scintillation vial in position A1 on slot 11.
3. 275 ul of each C9 WS-1, WS-2, WS-3 and WS-4 in positions B1-B4 of the tuberack on slot 7 is then transferred to the scintillation vial in position A2 on slot 11.
4. 275 ul of each C8 WS-1, WS-2, WS-3 and WS-4 in positions C1-C4 of the tuberack on slot 7 is then transferred to the scintillation vial in position A3 on slot 11.
5. 275 ul of each C7 WS-1, WS-2, WS-3 and WS-4 in positions A1-A4 of the tuberack on slot 8 is then transferred to the scintillation vial in position A4 on slot 11.
6. 275 ul of each C6 WS-1, WS-2, WS-3 and WS-4 in positions B1-B4 of the tuberack on slot 8 is then transferred to the scintillation vial in position B1 on slot 11.
7. 275 ul of each C5 WS-1, WS-2, WS-3 and WS-4 in positions C1-C4 of the tuberack on slot 8 is then transferred to the scintillation vial in position B2 on slot 11.
8. 275 ul of each C4 WS-1, WS-2, WS-3 and WS-4 in positions A1-A4 of the tuberack on slot 9 is then transferred to the scintillation vial in position B3 on slot 11.
9. 275 ul of each C3 WS-1, WS-2, WS-3 and WS-4 in positions B1-B4 of the tuberack on slot 9 is then transferred to the scintillation vial in position B4 on slot 11.
10. 275 ul of each C2 WS-1, WS-2, WS-3 and WS-4 in positions C1-C4 of the tuberack on slot 9 is then transferred to the scintillation vial in position C1 on slot 11.

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
0bc358-4

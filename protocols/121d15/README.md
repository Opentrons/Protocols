# Manual Cleave

### Author
[Opentrons](https://opentrons.com/)


# Opentrons has launched a new Protocol Library. This page won’t be available after March 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* Sample Prep
	* Plate Filling

## Description

Links:
* [Manual Cleave](./121d15)
<br />
<br />
* [Manual Cleave with Repeat for 2nd EDA](./121d15-repeat)
<br />
<br />
* [Manual Cleave Elution (Off-deck Vacuum)](./121d15-4)
<br />
<br />
* [Manual Cleave, ACN + Elution (Off-deck Vacuum)](./121d15-5)
<br />
<br />
* [Manual Cleave, ACN + Elution (On-deck Vacuum)](./121d15-6)
<br />
<br />
* [HPLC Picking](./121d15-3)
<br />
<br />
* [Redo Replacement Picking (Greiner MASTERBLOCK 96 Well Plate 500 µL)](./121d15-2-96-Greiner-500)
<br />
<br />
* [Redo Replacement Picking (Greiner MASTERBLOCK 96 Well Plate 1000 µL)](./121d15-2-96-Greiner-1000)
<br />
<br />
* [Redo Replacement Picking (Irish Life Sciences 96 Well Plate 2200 µL)](./121d15-2-96-Irish-2200)
<br />
<br />
* [Redo Replacement Picking (Greiner Masterblock 384 Well Plate 225 µL)](./121d15-2-384)
<br />
<br />
* [Aliquoting - 2ml Tuberack to 2ml Tuberack](./121d15-7-2ml-2ml-aliquot)
<br />
<br />
* [Aliquoting - 15ml Tuberack to 2ml Tuberack](./121d15-7-2ml-15ml-aliquot)
<br />
<br />
* [Pooling - 2ml Tuberack to 2ml Tuberack](./121d15-7-2ml-2ml-pool)
<br />
<br />
* [Pooling - 2ml Tuberack to 15ml Tuberack](./121d15-7-2ml-15ml-pool)
<br />
<br />

This protocol performs a custom plate filling for up to 4x 96-well plates from a single reagent reservoir. The user can input the number of rows and columns to be filled for each plate. Liquid handling parameters are automatically determined from the user's selection of which reagent will be added during the run.

---

### Labware
* Custom 96-tuberack
* [NEST 1 Reservoir 195ml](https://shop.opentrons.com/nest-1-well-reservoirs-195-ml/)
* [Opentrons 300µL Tips](https://shop.opentrons.com/opentrons-300ul-tips-1000-refills/)

### Pipettes
* [P300 8 Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)

### Reagents
* EDA
* ACN
* Amino

---

### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/121d15/deckv2.png)

---

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
121d15

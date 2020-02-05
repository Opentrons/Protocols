# PCR Preparation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* PCR preparation

## Description
This protocol performs a custom PCR preparation on DNA samples in triplicate using pre-created mastermix.

DNA sample tubes should be placed down columns before moving across rows (sample 1 in tuberack 1 tube A1, sample 2 in tuberack 1 tube B1, ..., sample 5 in tuberack 1 tube A2, etc.). If more than 24 samples are specified, the same pattern continues on a second tuberack for up to 12 more tubes (sample 25 in tuberack 2 tube A1, sample 26 in tuberack 2 tube B1, etc.).

Triplicates samples are filled in the PCR plate across rows before moving down columns (sample 1 in wells A1-A3, sample 2 in wells A4-A6, ..., sample 5 in B1-B3, etc.).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Thermo Scientific semi-skirted 96-well PCR plate 300ul #AB1400150](https://www.fishersci.com/shop/products/thermo-scientific-96-well-semi-skirted-plates-flat-deck-11/ab1400150?searchHijack=true&searchTerm=AB1400150&searchType=RAPID&matchedCatNo=AB1400150)
* [NEST 12-channel reservoir 15ml #360102](https://labware.opentrons.com/nest_12_reservoir_15ml?category=reservoir)
* [Opentrons 4x6 tuberacks with Eppendorf 1.5 mL safe-lock snapcap tubes](https://labware.opentrons.com/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap?category=tubeRack)
* [Opentrons P300 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons P20 single-channel GEN2 electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons 10/20ul and 50/300ul tipracks](https://shop.opentrons.com/collections/opentrons-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

4x6 tuberack 1 (slot 4):
* DNA samples 1-24

4x6 tuberack 2 (slot 5):
* DNA samples 24-36

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P300 multi-channel and P20 GEN2 single-channel pipettes and the number of DNA samples to process (1-32).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
640a85

# 022548-2 - Sample transfer and bead mastermix addition

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Nucleic Acid Extraction & Purification
	* DNA Extraction

## Description
This protocol transfers samples from tubes in up to 3 PRL tuberacks to a destination plate followed by resuspending a bead/binding buffer mastermix before transfering it to the samples on the plate.

Explanation of parameters below:
* `Number of samples in tuberack 1 slot(2-3)`: How many samples to transfer from rack 1: 1 to 32
* `Number of samples in tuberack 2 (slot 4-5)`: 0 to 32
* `Number of samples in tuberack 3 (7-8)`: 0 to 32
* `Master mix wells location`: Informs the protocol which wells of the reservoir contain mastermix, for example 5-10 to specify wells A5 to A10. This parameter may also be a single number instead of a range
* `Mastermix max volume per well (mL)`: Informs the protocol what the maximal volume of mastermix is in each reservoir well, default is 9.54 mL
* `Mastermix mixing rate multiplier`: Controls the flow rate of mixing, 1.0 means standard flow rate, less is slower and more is faster.
* `mastermix aspiration flow rate multiplier`: Controls the rate of aspiration of mastermix from the reservoir wells
* `mastermix dispension flow rate multiplier`: Controls the rate of dispension of mastermix into wells on the target plate
* `Mount for 300 uL single channel pipette`: Left or right
* `Mount for 300 uL multi channel pipette`: Left or right
* `Pause after mixing the mastermix for vortex/resuspension?`: Optional pause after (re-)mixing the mastermix where the reservoir may be taken out for manual resuspension such as vortexing, nutation or shaking if resuspension by pipetting is deemed insufficient.

---

### Labware
* [NEST 12-Well Reservoirs, 15 mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* PRL tuberack for 32 15 mL tubes
* [Thermo Fisher Kingfisher 96 deepwell plate 2 mL](https://www.thermofisher.com/order/catalog/product/A43075)


### Pipettes
* [P300 multi-Channel (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [P300 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [300 uL tipracks](https://shop.opentrons.com/opentrons-300ul-tips-1000-refills/)
* [Opentrons 200 µL filter tiprack](https://shop.opentrons.com/opentrons-200ul-filter-tips/)

---

### Deck Setup
Slot 1: Target - Kingfisher 96 well plate
Slot 2-3: PRL 32 15 mL tuberack
Slot 4-5: PRL 32 15 mL tuberack
Slot 6: 200 uL Opentrons filter tiprack
Slot 7-8: PRL 32 15 mL tuberack
Slot 9: 300 uL Opentrons tiprack
Slot 10: Mastermix reservoir
![Deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/022548/2/deck.jpg)

### Reagent Setup
* Mastermix Reservoir: Specify what wells contain mastermix in the parameter section - See parameter section above.

---

### Protocol Steps
1. Transfer samples from the tubracks to the target plate in row order using the single channel 300 uL pipette using 200 uL filter tips.
2. Mix the bead/binding buffer mastermix 7 times.
3. Remove tips from the 300 uL tiprack that do not correspond to sample wells on the target plate.
3. Transfer mastermix to samples using the multi-channel 300 uL pipette with regular 300 uL tips.

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
022548-2

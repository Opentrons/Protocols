# Extraction Prep for TaqPath Covid-19 Combo Kit

### Author
[Opentrons](https://opentrons.com/)

### Partner
[appliedbiosystems](https://www.thermofisher.com/content/dam/LifeTech/Documents/PDFs/clinical/taqpath-COVID-19-combo-kit-full-instructions-for-use.pdf)

## Categories
* Sample Prep
	* Plate Filling

## Description
This protocol preps a sample plate with up to 95 samples (with one control) as well as the necessary ethanol, buffer, and elution solution blocks. Mag beads are added to the sample. The protocol pauses if more than 45 samples are run to allow the user to replace sample tube racks.

Explanation of complex parameters below:
* `Number of samples`: Specify the number of samples that will be processed. Up to 95 samples can be run, leaving room for a control.
* `P1000 sample tube aspiration height`: Specify the height (in mm) for the P1000 pipette to aspirate when visiting sample tubes. Default is 1mm.
* `MagBead mix speed`: Specify the speed (in ul/sec) to mix mag beads.
`P1000 aspiration/dispense speed for mag bead transfer`: Specify the aspiration/dispense speed for mag bead transfer of the p1000 pipette.
* `P20 single GEN2 Mount`: Specify which mount (left or right) to load the P20 single channel pipette.
* `P1000 single GEN2 Mount`: Specify which mount (left or right) to load the P1000 single channel pipette.
---
### Labware
* [NEST 2 mL 96-Well Deep Well Plate, V Bottom](https://shop.opentrons.com/collections/lab-plates/products/nest-0-2-ml-96-well-deep-well-plate-v-bottom)
* [Opentrons 20µL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 1000uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [Nest 12 Well Reservoir 15mL](https://shop.opentrons.com/collections/reservoirs)
* [Nest 1 Well Reservoir 195mL](https://shop.opentrons.com/collections/reservoirs)

### Pipettes
* [P1000 GEN2 Single Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P300 GEN2 Multi Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette)

### Reagents
* [TaqPath Covid-19 Combo Kit](https://www.thermofisher.com/content/dam/LifeTech/Documents/PDFs/clinical/taqpath-COVID-19-combo-kit-full-instructions-for-use.pdf)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0d2950/Screen+Shot+2021-07-27+at+5.33.11+PM.png)

### Reagent Setup


![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0d2950/Screen+Shot+2021-07-27+at+5.33.37+PM.png)


---

### Protocol Steps
1. Buffer plate made according to total number of samples.
2. Ethanol plate made according to total number of samples.
3. Elution plate made according to total number of samples.
4. Samples placed on sample block. Protocol pauses if running more than 45 samples to replace sample tube racks. If replacing tube racks, samples should be loaded down by column starting from slot 1, then to slot 2 and so on.
5. Mag beads added to samples with pre-mix step to resuspend beads.




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
0d2950

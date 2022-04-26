# Omega Bio-Tek Mag-Bind Plant DNA DS Kit

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Nucleic Acid Extraction & Purification
	* Omega Bio-Tek Mag-Bind Plant DNA DS Kit

## Description
This protocol automates the [Omega Bio-Tek Mag-Bind® Plant DNA DS 96 Kit](https://www.omegabiotek.com/product/plant-extraction-mag-bind-plant-dna-ds-96/) on the OT-2.

Using the [P300 8-Channel Pipette, GEN2](https://shop.opentrons.com/8-channel-electronic-pipette/) all liquid handling steps outlined in [the protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-12-14/kf03tt7/Omega%20BioTek%20Mag-Bind%20Plant%20DNA%20extraction%20automation%20protocol.pdf) are handled on the OT-2, with minimal user intervention. To optimize liquid handling on the automated platform, some reagents should be combined prior to adding to the deck (more details below).

Explanation of complex parameters below:
* **Pipette Mount**: Select which mount (left or right) the [P300 8-Channel Pipette, GEN2](https://shop.opentrons.com/8-channel-electronic-pipette/) is attached to.
* **Number of Samples**: Specify the number of samples (1-96). Please note ~ because the 8-channel pipette is used in this protocol, any number will be rounded up to 8.
* **Labware for Input Samples**: Type the [API load name](https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols) of the labware containing samples.
* **Elution Volume (in µL)**: The volume of Elution Buffer added to each well. Please note ~ [the written protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-12-14/kf03tt7/Omega%20BioTek%20Mag-Bind%20Plant%20DNA%20extraction%20automation%20protocol.pdf) states 100-200µL and this protocol has been designed accordingly.

*Note*: This protocol was updated on April 13th, 2022

---

### Modules
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Labware
* Sample Input Labware (specified in parameters)
* [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* [NEST 1-Well Reservoir, 195mL](https://shop.opentrons.com/nest-1-well-reservoirs-195-ml/)
* [NEST 96-Well PCR Plate](https://shop.opentrons.com/nest-0-1-ml-96-well-pcr-plate-full-skirt/)
* [NEST 96-Well Deepwell Plate, 2mL](https://shop.opentrons.com/nest-2-ml-96-well-deep-well-plate-v-bottom/)
* [Opentrons 200µL Filter Tip Rack(s)](https://shop.opentrons.com/opentrons-200ul-filter-tips/)

### Pipettes
* [P300 8-Channel Pipette, GEN2](https://shop.opentrons.com/8-channel-electronic-pipette/)


### Reagents
* [Omega Bio-Tek Mag-Bind® Plant DNA DS 96 Kit](https://www.omegabiotek.com/product/plant-extraction-mag-bind-plant-dna-ds-96/)

---

### Deck Setup
![Deck Layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/3e0bef/3e0bef_deck.png)

### Reagent Setup
Reagents for this protocol are split between two [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/). For each reagent, a section of 2-6 channels are dedicated and when transferring to samples, channels are used sequentially. For example, the CSPW2 Buffer can be split across 4 channels. In this example, each channel can hold enough reagent for up to 3 columns of samples (24 total samples). Continuing with this example, if 32 samples were being processed, enough reagent for 3 columns of sample would fill the first dedicated channel for the CSPW2 Buffer and enough reagent for 1 column would fill the second channel.</br>
</br>
When determining the amount of reagent, the number of sample columns should be multiplied by eight, 1.1 (an additional 10%), and the amount of reagent needed. Based on the number of channels dedicated to each reagent, the amount needed in each channel can be calculated.</br>
</br>
**Reservoir 1: Deck Slot 2**</br>
CSPL Buffer (700µL per sample) + Proteinase K (20µL per sample): Channels 1-6</br>
RNase A (5µL) + RBB Buffer (500µL) + Mag-Bind Beads (20µL): Channels 1-6 (after replacing)</br>
CSPW1 Buffer (500µL): Channels 7-10</br>
Elution Buffer: Channels 11-12 (added at 65C prior to liquid handling step)</br>
![Reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/3e0bef/3e0bef_res1.png)
</br>
</br>
**Reservoir 2: Deck Slot 3**</br>
CSPW2 Buffer (500µL): Channels 1-4</br>
SPM Buffer, Wash 1 (500µL): Channels 5-8</br>
SPM Buffer, Wash 2 (500µL): Channels 9-12</br>
![Reservoir 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/3e0bef/3e0bef_res2.png)

---

### Protocol Steps
1. The protocol begins by adding 720µL of CSPL Buffer + Proteinase K (700+20) to each column in the 96-Well Plate containing the starting samples.
2. User is prompted to perform off deck incubation.
3. Once the sample plate is returned to the deck, 500µL is transferred to the 96-Well Deepwell plate.
4. 525µL of RNase A + RBB Buffer + Mag-Bind Beads (5+500+20) is transferred to each column containing samples.
5. After incubating, the Mag Deck engages, and after the pellet forms, 1025µL is transferred to the NEST 1-Well Reservoir for liquid waste.
6. 500µL of CSPW1 Buffer is added to each column of samples and mixed.
7. After incubating on the Mag Deck, 500µL is transferred to the liquid waste.
8. 500µL of CSPW2 Buffer is added to each column of samples and mixed.
9. After incubating on the Mag Deck, 500µL is transferred to the liquid waste.
10. 500µL of SPM Buffer (wash 1) is added to each column of samples and mixed.
11. After incubating on the Mag Deck, 500µL is transferred to the liquid waste.
12. 500µL of SPM Buffer (wash 2) is added to each column of samples and mixed.
13. After incubating on the Mag Deck, 500µL is transferred to the liquid waste.
14. A 10 minute incubation begins, at which point, the user should fill the reagent reservoir with the warmed Elution Buffer.
15. Once the incubation period is over, the Elution Buffer is added to the samples on the Mag Deck.
16. The user is prompted to remove the Plate on the Mag Deck and incubate at 65C.
17. Once the incubation is complete, the user returns the Plate to the Mag Deck.
18. The Mag Deck engages and after the pellet forms, the elution is transferred to the PCR plate.

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
3e0b3f

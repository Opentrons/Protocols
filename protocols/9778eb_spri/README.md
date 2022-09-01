# SPRI Bead Purification, Size Selection

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Nucleic Acid Extraction & Purification
	* SPRI Beads

## Description
This protocol purifies samples using SPRI beads with an option to perform a size selection with two separate bead ratios. Size selection requires two magnetic modules.

Beads are added at a specified ratio to the samples, mixed, and left to incubate. If size selection is to be performed, the supernatant is then removed to the second magnetic module for a second bead purification where the resulting supernatant is removed to the liquid waste.

After bead purification(s), two 200uL ethanol washes are performed. The beads are left to air dry for a set amount of time before a set volume of elution liquid is added, mixed with the beads, left to incubate for a set time, and separated from the beads. This supernatant is removed to an awaiting plate in slot 3.

Explanation of complex parameters below:
* `Number of Samples`: How many samples are in the starting 96 well plate, 1-96 allowed. Multiples of 8 for full columns will have the most efficient reagent use
* `Initial Sample Volume`: Volume in uL for starting samples. This is used to help calculate bead volume addition
* `Bead Ratio 1`: Bead to sample ratio used to calculate bead volume addition. First addition for size selection and only addition for non-size selection
* `Bead Ratio 2`: Bead to sample ratio used to calculate bead volume addition for second bead addition during size selection. This is not used during non-size selection protocols with a single bead addition
* `Transfer Volume`: During size selection, how much volume to transfer from first magnetic module plate to second. This is needed to properly calculate second bead addition volume for proper size selection
* `Bead Air Dry Time`: How many minutes beads will be left to air dry after ethanol wash steps. Default is 10 minutes
* `Bead Incubation Time`: How many minutes beads will be left to incubate with samples during first and second addition. Default is 5 minutes
* `Bead Separation Time`: How many minutes beads will be left to separate on the magnetic module. Default is 5 minutes
* `Elution Solution Volume`: How much liquid will be added to washed and dried beads for elution. Default volume is 50 uL
* `Elution Time`: How many minutes the elution solution will incubate with the beads. Default is 10 minutes
* `Final Plate Volume`: How much liquid will be transferred from the beads mixed with elution liquid to final elution plate in slot 3. Default is 50 uL
* `Flash Robot on Pause`: Set whether the OT-2 will flash when trash is full, tips need refilling, or general user intervention is needed. Default is flashing.
* `P300 Multi Channel Pipette Mount`: Select which mount side the p300 multichannel pipette is connected to. Default is left. The p20 multichannel will be set to the opposite side.
* `Size Selection or Single Purification`: Select whether the OT-2 will perform a single bead purification with one magnetic module or a dual bead ratio-based size selection with two magnetic modules. Default is size selection.

---

### Modules
* [Magnetic Module (GEN2) x2](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Labware
* [NEST 12 Well Reservoir 15 mL](https://labware.opentrons.com/nest_12_reservoir_15ml)
* [NEST 1 Well Reservoir 195 mL](https://labware.opentrons.com/nest_1_reservoir_195ml)
* Custom 3D printed custom adapter for half-skirted plates with below half-skirted plate
* [Thermofisher PCR Plate, 96-well, semi-skirted, flat deck, black lettering](https://www.thermofisher.com/order/catalog/product/AB1400L)

### Pipettes
* [Opentrons P300 8 Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [Opentrons P20 8 Channel Electronic Pipette (GEN20)](https://shop.opentrons.com/8-channel-electronic-pipette/)

### Reagents
* [SPRI Beads](https://www.beckman.com/reagents/genomic/cleanup-and-size-selection/size-selection?utm_medium=cpc&utm_source=google&utm_campaign=ecommerce-spriselect&utm_content=geno_ecommerce_bottom&creative=443930351713&keyword=spri%20beads&matchtype=e&network=g&device=c&gclid=Cj0KCQjwjbyYBhCdARIsAArC6LI6dgI3lnL2E7_tB8sJuHRyIDWJx124iGVRfQQ-k2MabecsakRC6U4aAsf_EALw_wcB)

---

### Deck Setup
* Reagent Color Code
![color code](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)
* Starting deck layout with reagents
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

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

# Fetal DNA NGS library preparation part 4 - LifeCell NIPT 35Plex HV - Post-PCR cleanup and preparation for quantification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* DNA Library prep

## Description
This protocol mixes end-repaired DNA samples with adaptor ligation mastermix and DNA barcodes specified according to a CSV input file

### Parameters
* `Number of samples`: The number of DNA samples on your sample plate. Should be between 7 and 36.

* `Magnetic engagement time when total sample volume < 50 uL`: How many minutes to engage the magnets when the total bead sample volume is 50 µL or less, Opentrons recommends 5 minutes.

* `Magnetic engagement time when total sample volume > 50 uL`: How many minutes to engage the magnets when the total bead sample volume is more than 50, Opentrons recommends 7 minutes.
---

### Labware
* TBD

### Pipettes
* [P300 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P20 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/459cc2/459cc2-layout.png)

### Reagent Setup
* Slot 1 Destination Plate 5 (DP-5) - Samples for quantification/normalization
* Slot 2 Destination Plate 3 (DP-3) - PCR amplification DNA from Part 3
* Slot 3 Magnetic module with Destination plate 4 (DP-4) - For cleaning up the DNA on DP-3
* Slot 4 Empty
* Slot 5 200 µL Opentrons filter tips
* Slot 6 12-well reservoir (Well 1: 80 % EtOH, Well 2: nuc. free water, Well 3: Qubit workin solution, Well 12: Liquid waste)
* Slot 7 Empty
* Slot 8 200 µL Opentrons filter tips
* Slot 9 Paramagnetic Bead Reagent plate 2
* Slot 10 20 µL Opentrons filter tips
* Slot 11 20 µL Opentrons filter tips

---

### Protocol Steps
1. Transfer 25 µL of PCR amplified DNA sample to DP-4 on the magnetic module
1. Mix the paramagnetic beads and add 25 µL to the samples on DP-2/magnetic module
2. Ask the user to spin down the plate for 5 seconds
3. Engage the magnets and incubate the beads according to the time parameter when total volume is < 50 µL
4. Discard the supernatant
5. Wash the beads in 75 µL 80 % ethanol and discard the supernatant (2 times). The magnets remain engaged throughout
6. Ask the user to spin down the plate
7. Remove any remaining supernatant
8. Air dry the beads for 5 minutes
9. The bead containing samples are resuspended in 22 µL of nuc. free water
10. 20 µL of the resuspended DNA is transferred to DP-5
11. Quantification samples are created on DP-5 starting at column 6 (Well A6)
12. 198 µL of Qubit HS working solution is transferred to DP-5/column 6
13. 2 µL of DNA sample is transferred to each corresponding DP-5/column 6 well
14. The user is asked to vortex the plate and incubate for 2 minutes before proceeding

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
466f93-4

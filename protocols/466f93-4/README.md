# Fetal DNA NGS library preparation part 4 - LifeCell NIPT 35Plex HV - Post-PCR cleanup and preparation for quantification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep

## Description
This protocol cleans up the PCR reaction from the previous step and prepares samples for DNA quantification using the Qubit HS protocol.

* `Number of samples`: The number of DNA samples on your sample plate. Should be between 7 and 36.

* `Magnetic engagement time`: How many minutes to engage the magnets in order to bind paramagnetic beads. Opentrons recommends at least 5 minutes for volumes less than 50 µL. 

---

### Labware
* [Bio-Rad 96 well 200 µL PCR plate](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr?category=wellPlate)
* [NEST 12-well reservoir](https://labware.opentrons.com/nest_12_reservoir_15ml/)

### Pipettes
* [P300 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P20 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Opentrons 96 Filter Tip Rack 20 µL](https://labware.opentrons.com/opentrons_96_filtertiprack_20ul/)
* [Opentrons 96 Filter Tip Rack 200 µL](https://labware.opentrons.com/opentrons_96_filtertiprack_200ul/)

---

### Deck Setup

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/466f93/deck_state_part4_466f93.jpeg)

![reservoir layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/466f93/reservoir_layout_466f93_part4.jpeg)

### Reagent Setup
* Slot 1 Destination Plate 5 (DP-5) - Samples for quantification/normalization
* Slot 2 Destination Plate 3 (DP-3) - PCR amplification DNA from Part 3
* Slot 3 Magnetic module with Destination plate 4 (DP-4) - For cleaning up the DNA on DP-3
* Slot 4 Empty
* Slot 5 200 µL Opentrons filter tips
* Slot 6 12-well reservoir (Well 1: 80 % EtOH, Well 2: nuc. free water, Well 3: Qubit working solution (9 mL), Well 12: Liquid waste)
* Slot 7 Empty
* Slot 8 200 µL Opentrons filter tips
* Slot 9 Paramagnetic Bead Reagent plate 2
* Slot 10 20 µL Opentrons filter tips
* Slot 11 20 µL Opentrons filter tips

---

### Protocol Steps
1. The user places all the required labware on the deck and makes sure to replace any used or partially used tip racks
2. Transfer 25 µL of PCR amplified DNA sample to DP-4 on the magnetic module
3. Mix the paramagnetic beads and add 25 µL to the samples on DP-4 on the magnetic module
4. Ask the user to spin down the plate for 5 seconds
5. Engage the magnets and incubate the beads according to the time parameter
6. Discard the supernatant
7. Wash the beads in 75 µL 80 % ethanol and discard the supernatant (repeat step 2 times). The magnets remain engaged throughout
8. Ask the user to spin down the plate
9. Remove any remaining supernatant
10. Air dry the beads for 5 minutes
11. The bead containing samples are resuspended in 22 µL of nuc. free water
12. 20 µL of the resuspended DNA is transferred to DP-5 (clean DNA and quantification plate) in sequence starting at well A1
13. Quantification samples are created on DP-5 starting at column 6 (Well A6) in sequence.
14. 198 µL of Qubit HS working solution is transferred to the quantification samples starting at DP-5/column 6
15. 2 µL of DNA sample is transferred to each corresponding DP-5/column 6 well
16. The user is asked to vortex the plate and incubate for 2 minutes before proceeding.
17. The user transfers the Qubit samples manually to appropriate vessels for the Qubit HS procedure and performs the quantification, and creates a CSV file as described in part 5.

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

# Fetal DNA NGS library preparation part 3 - LifeCell NIPT 35Plex HV - DNA cleanup and PCR amplification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep

## Description
This protocol cleans up barcoded DNA using paramagnetic beads. After cleanup the clean DNA is mixed with primers and PCR mastermix and is ready for PCR.

* `Number of samples`: The number of DNA samples on your sample plate. Should be between 7 and 36.

* `Magnetic engagement time`: How many minutes to engage the magnets when the total bead sample volume is 50 µL or less, Opentrons recommends at least 5 minutes.

---

### Labware
* [Bio-Rad 96 well 200 µL PCR plate](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr?category=wellPlate)
* [NEST 12-well reservoir](https://labware.opentrons.com/nest_12_reservoir_15ml/)
* [Magnetic module GEN2](https://shop.opentrons.com/magnetic-module-gen2/)

### Pipettes
* [P300 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P20 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Opentrons 96 Filter Tip Rack 20 µL](https://labware.opentrons.com/opentrons_96_filtertiprack_20ul/)
* [Opentrons 96 Filter Tip Rack 200 µL](https://labware.opentrons.com/opentrons_96_filtertiprack_200ul/)

---

### Deck Setup

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/466f93/deck_state_part3_466f93.jpeg)

![reservoir layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/466f93/reservoir_layout_466f93_part4.jpeg)

### Reagent Setup
* Slot 1 Empty
* Slot 2 Destination Plate 3 (DP-3) - PCR amplification
* Slot 3 Magnetic module GEN2 with DP-2 - End-repaired and barcoded samples
* Slot 4 Empty
* Slot 5 200 µL Opentrons filter tips
* Slot 6 12-well reservoir. Well 1: Nuc. free water (5 mL), Well 2: 80 % Ethanol (12 mL), Well 12: Liquid waste
* Slot 7 Yourgene cfDNA Library Prep Kit Library Preparation Plate I
* Slot 8 200 µL Opentrons filter tips
* Slot 9 Paramagnetic Bead reagent plate 2
* Slot 10 20 µL Opentrons filter tips
* Slot 11 20 µL Opentrons filter tips

---

### Protocol Steps
1. The user places all the required labware on the deck and makes sure to replace any used or partially used tip racks
2. Mix the paramagnetic beads and add to the samples on DP-2/magnetic module
3. Ask the user to spin down the plate
4. Engage the magnets and incubate the beads according to the time parameter when total volume is < 50 µL
5. Discard the supernatant
6. Wash the beads in 80 % ethanol and discard the supernatant (2 times)
7. Ask the user to spin down the plate
8. Remove any remaining supernatant
9. Air dry the beads for 5 minutes
10. Resuspend the beads in nuclease free water (Reservoir well 2)
11. Transfer resuspended DNA to DP-3
12. Create a PCR (super-)mastermix consisting of the PCR mastermix plus the primers. This super-mastermix is created in wells C10 to E10 of Yourgene Reagent plate 1.
13. The super-mastermix is distributed to the DNA samples on DP-3
14. The user is asked to spin down DP-3 and perform the PCR step described in 1.2.47

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
466f93-3

# Fetal DNA NGS library preparation part 3 - LifeCell NIPT 35Plex HV - DNA cleanup and PCR amplification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* DNA Library prep

## Description
This protocol mixes end-repaired DNA samples with adaptor ligation mastermix and DNA barcodes specified according to a CSV input file

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
* Slot 1 Empty
* Slot 2 Destination Plate 3 (DP-3) - PCR amplification
* Slot 3 Magnetic module with DP-2 - End-repaired and barcoded samples
* Slot 4 Empty
* Slot 5 200 µL Opentrons filter tips
* Slot 6 12-well reservoir (not used in part 2)
* Slot 7 Yourgene cfDNA Library Prep Kit Library Preparation Plate I
* Slot 8 200 µL Opentrons filter tips
* Slot 9 Paramagnetic Bead reagent plate 2
* Slot 10 20 µL Opentrons filter tips
* Slot 11 20 µL Opentrons filter tips

---

### Protocol Steps
1. Mix the paramagnetic beads and add to the samples on DP-2/magnetic module
2. Ask the user to spin down the plate
3. Engage the magnets and incubate the beads according to the time parameter when total volume is < 50 µL
4. Discard the supernatant
5. Wash the beads in 80 % ethanol and discard the supernatant (2 times)
6. Ask the user to spin down the plate
7. Remove any remaining supernatant
8. Air dry the beads for 5 minutes
9. Resuspend the beads in nuclease free water
10. Transfer resuspended DNA to DP-3
11. Create a PCR (super-)mastermix consisting of the PCR mastermix plus the primers. This super-mastermix is created in wells C10 to E10 of Yourgene Reagent plate 1.
12. The super-mastermix is distributed to the DNA samples on DP-3
13. The user is asked to spin down DP-3 and perform the PCR step described in 1.2.47

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

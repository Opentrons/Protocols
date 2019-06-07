# Nucleic Acid Purification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
		* Nucleic Acid Purification

## Description
This protocol performs nucleic acid purification using an Opentrons magnetic module. The final elution is transferred to a fresh plate to finish the protocol. For reagent setup, see 'Additional Notes' below.

---

You will need:
* [Opentrons P50 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [Opentrons P300 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [Opentrons 300ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [FrameStar 96 Well Semi-Skirted PCR Plate](https://www.4ti.co.uk/new-products/framestar-96-well-roche-style-plates-high-sensitivity)
* [12-Channel trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [MagDeck](https://shop.opentrons.com/collections/labware/products/magdeck)

### Reagents
* [KAPA HiFi Hotstart ReadyMix (2x) no. KK2601](https://www.kapabiosystems.com/product-applications/products/pcr-2/kapa-hifi-pcr-kits/)
* [Agencourt Ampure XP beads (Beckman Coulter # A 63881)](https://www.beckman.com/reagents/genomic/cleanup-and-size-selection/pcr/a63881)
* Ethanol

## Process
1. Input the number of sample columns to run (max 12).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Ampure XP beads are mixed and transferred to each sample on the sample plate (loaded on the disengaged magdeck). Samples are mixed after the transfer, and a new tip is used for each transfer/mix action to avoid contamination.
8. Samples incubate at room temperature for 8 minutes for the DNA to bind to the beads. Then, the magdeck engages, and the samples incubate for an additional 5 minutes for the beads to separate.
9. Supernatant is removed and disposed in the liquid trash.
10. Ethanol is transferred to the first column of samples on the engaged magdeck. The samples incubate for 30 seconds, and the ethanol is removed using the same tips.
11. Step 10 is repeated with new tips for as many sample columns as specified.
12. Steps 10-11 are repeated 1x more for a total of 2 ethanol washes.
13. The samples dry at room temperature for 5 minutes, and the magdeck disengages.
14. Elution buffer is transferred to each sample on the disengaged magdeck. Samples are mixed after the transfer, and a new tip is used for each transfer/mix action to avoid contamination.
15. The samples incubate for 2 minutes. Then, the magdeck engages, and the samples incubate for an additional 2 minutes for the beads to separate.
16. The protocol pauses and prompts the user to load the fresh plate for elution if not done already.
17. Elution from each sample is transferred to its corresponding well on the fresh plate. New tips are used for each transfer to avoid contamination.

### Additional Notes
Trough setup:
![trough setup](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1545/trough_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
4wyjHAyF  
1545

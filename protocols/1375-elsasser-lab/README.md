# AMPure DNA Clean-Up

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
Clean up to 96 samples in a 96 PCR plate with AMPure XP Beads.

---
1. Mix and transfer beads to each sample with P50 single-channel pipette, use new tip each time.
2. Incubate beads in RT for 5 minutes. Engage MagDeck and wait for 5 minutes.
3. Remove supernatant with P300 multi-channel pipette, use new tip each time.
4. Wash beads with 200 uL ethanol twice, reuse tips for the same sample.
5. Dry beads for 5 minutes. Disengage MagDeck.
6. Elute DNA in elution buffer, and transfer eluted DNA to new plate.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [MagDeck](https://shop.opentrons.com/products/magdeck)

### Reagents
* AMPure XP Beads

## Process
1. Input the number of samples you are processing.
2. Input the container in which you are putting the beads.
3. Input the location of the container in which you are putting the beads. (see Addtional Notes)
4. Input the volume of beads to be transferred to each sample.
5. Input the container in which you are putting the elution buffer.
6. Input the location of the container in which you are putting the elution buffer. (see Addtional Notes)
7. Input the volume of elution buffer to be transferred to each sample.
8. Download your protocol.
9. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
10. Set up your deck according to the deck map.
11. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
12. Hit "Run".

### Additional Notes
Reagent Setup:
* Ethanol: Trough A1
* Beads and Elution: make sure the locations are unique to all other reagents
* If trough is selected, please make sure not to use A1 since it is already reserved for Ethanol

###### Internal
oNe9RXr0
1375

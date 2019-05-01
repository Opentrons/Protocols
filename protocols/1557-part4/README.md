# Ion AmpliSeq Library Prep 4/4: Library Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* NGS Library Prep
    * Ion AmpliSeq Library Prep

## Description
Links:
* [Part 1: DNA Target Amplification](./1557-part1)
* [Part 2: Partially Digest Amplicons](./1557-part2)
* [Part 3: Ligate Adapters](./1557-part3)
* [Part 4: Library Purification](./1557-part4)

---
You will need:
* [P300 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5978988707869)
* [Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Twin.tec skirted PCR Plate](https://www.fishersci.com/shop/products/eppendorf-96-well-twin-tec-pcr-plates-yellow-skirted-150-l/e951020427)
* PCR Strip Tubes
* 12-well Trough
* Neptune 10 uL Filter Tips

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the number of samples you are processing. (MAX=24)
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 45 uL AMPure XP Beads to each sample.
8. Robot will engage the Magnetic Module and remove supernatant.
9. Robot will wash the plate with 150 uL 70% ethanol.
10. Robot will remove supernatant and dry the plate for 5 minutes.
11. Robot will transfer elution buffer to the samples.
12. Robot will transfer supernatant to a new plate.


### Additional Notes

Place the sample plate on the Magnetic Module to begin the protocol.

---

Trough:
* AMPure XP Beads: A1
* 70% Ethanol: A2
* Elution Buffer: A3

---

Clean Twin.tec skirted PCR Plate: slot 1

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
D2AAz1dg
1557

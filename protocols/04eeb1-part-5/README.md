# Illumina COVIDSeq Test: Tagment PCR Amplicons

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
	* Illumina COVIDSeq Test

## Description
The Illumina COVIDSeq Test is a high-throughput, next-generation sequencing test that is used fo detecting SARS-CoV-2 in patient samples. This protocol is the fifth part of a seven-part protocol that is run on the OT-2 for this kit.

* Part 1: Anneal RNA
* Part 2: Synthesize First Strand cDNA
* Part 3: Amplify cDNA
* Part 4: Tagment PCR Amplicons
* Part 5: Post Tagmentation Clean Up
* Part 6: Amplify Tagmented Amplicons
* Part 7: Pool and Clean Up Libraries

Explanation of complex parameters below:
* `P300 Multichannel GEN2 Pipette Mount`: Choose the mount position of your P20 Multichannel pipette, either left or right.

---

### Modules
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Labware
* [Opentrons 200 uL Filter Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-200ul-filter-tips)
* [Bio-Rad Hard-Shell 96 Well Plate 200 µL PCR](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr/)
* [NEST 12-Well Reservoirs, 15 mL](https://shop.opentrons.com/collections/reservoirs/products/nest-12-well-reservoir-15-ml)

### Pipettes
* [P300 8-Channel Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette)

### Reagents
* [Illumina COVIDSeq Test](https://www.illumina.com/products/by-type/ivd-products/covidseq.html)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/04eeb1/04eeb1-part-5.png)

**Note**: Wash Buffer should be added in Column 2 (A2).

---

### Protocol Steps
1. Engage Magnetic Module and wait 3 minutes for beads to pellet.
2. Pick up 200 uL tips from slot 4
3. Aspirate 60 uL from Column 1 (A1) of the Magnetic Plate on Slot 3
4. Dispense into trash and discard tips.

**Steps 2-4 will repeat for the entire plate. This step also included a 10 uL residual volume.**

5. Pick up 200 uL tips from slot 4
6. Aspirate 100 uL of Wash Buffer
7. Dispense 100 uL of Wash Buffer into Column 1 (A1) of the Magnetic Plate on Slot 3
8. Discard tips into the trash

**Steps 5-8 will repeat for the entire plate.**

9. Disengage Magnets
10. Pause Protocol: Seal, Shake and Centrifuge. Then place back on the Magnetic Module and click Resume.
11. Engage Magnetic Module and wait 3 minutes for beads to pellet.
12. Pick up 200 uL tips from slot 4
13. Aspirate 100 uL of supernatant from Column 1 (A1) of the Magnetic Plate on Slot 3
14. Dispense into trash and discard tips.

**Steps 12-14 will repeat for the entire plate. This step also included a 10 uL residual volume.**

15. Repeat Steps 5-8.


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
04eeb1-part-5
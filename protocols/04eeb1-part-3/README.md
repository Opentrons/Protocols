# Illumina COVIDSeq Test: Amplify cDNA

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
	* Illumina COVIDSeq Test

## Description
The Illumina COVIDSeq Test is a high-throughput, next-generation sequencing test that is used fo detecting SARS-CoV-2 in patient samples. This protocol is the third part of a seven part protocol that is run on the OT-2 for this kit.

* Part 1: Anneal RNA
* Part 2: Synthesize First Strand cDNA
* Part 3: Amplify cDNA
* Part 4: Tagment PCR Amplicons
* Part 5: Post Tagmentation Clean Up
* Part 6: Amplify Tagmented Amplicons
* Part 7: Pool and Clean Up Libraries

Explanation of complex parameters below:
* `P20 Multichannel GEN2 Pipette Mount`: Choose the mount position of your P20 Multichannel pipette, either left or right.

---

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
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/04eeb1/04eeb1-part-3_layout.png)

**Note**: Master Mix should be added in Column 1 (A1) and Column 12 (A12) of the 12-well reservoir.

---

### Protocol Steps
1. Pick up tips from Opentrons 96 Filter Tip Rack 200 µL on Slot 10
2. Aspirate 200 uL from Column 1 (A1) of Master Mix Reservoir
3. Dispense 20 uL into Column 1 (A1) of Plate 1 on Slot 11

**Steps 3 will repeat for the entire plate.**

4. Drop tips into Opentrons Fixed Trash Bin

**Plate 2 Begins**

5. Pick up tips from Opentrons 96 Filter Tip Rack 200 µL on Slot 10
6. Aspirate 200 uL from Column 12 (A12) of Master Mix Reservoir
7. Dispense 20 uL into Column 1 (A1) of Plate 1 on Slot 7

**Steps 7 will repeat for the entire plate.**

8. Drop tips into Opentrons Fixed Trash Bin

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
04eeb1-part-3
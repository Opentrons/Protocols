# Extraction for PCR/qPCR prep

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Nucleic Acid Extraction & Purification
	* Nucleic Acid Extraction

## Description
This protocol preps up to 12 columns of samples for PCR/qPCR. Reagent A is first added to the plate up the specified number of columns, then samples are reformatted from four tube racks to a 96 well plate on the magnetic module. The four tube racks exactly mirror the 96 well plate, and transfers are done one-to-one between the tube rack and plate by column (A1-D1 of tube racks on slot 4 then 1, A2-D2 of tube racks on slot 4 then 1, so on and so forth). Samples are then mixed, magnet engaged, and supernatant removed. After incubation period, reagent B is added, and the process is repeated through reagent C.


Explanation of complex parameters below:
* `Number of Columns`: Specify the number of columns on the magnetic plate to process.
* `Incubation Time`: Specify the incubation time in minutes
* `P300 Single Mount`: Specify which mount (left or right) to host the P300 single-channel pipette
* `P300 Multi-Mount`: Specify which mount (left or right) to host the P300 multi-channel pipette

---

### Modules
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Labware
* [StorPlate-96V, PP, 96 well, V-bottom, (V), 450µL](https://www.perkinelmer.com/product/storplate-96-v-450-l-50-6008290)
* [Opentrons 200ul filter tips](https://shop.opentrons.com/collections/opentrons-tips)
* [Nest 12 well Reservoir, 15mL](https://shop.opentrons.com/collections/reservoirs/products/nest-12-well-reservoir-15-ml)
* [Nest 1 well Reservoir, 195mL](https://shop.opentrons.com/collections/reservoirs/products/nest-1-well-reservoir-195-ml)
* [Opentrons 4-in-1 tube rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)

### Pipettes
* [Opentrons P300 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [Opentrons P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette)

---

### Deck Setup

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

---

### Protocol Steps
1. Samples added to plate, NEST 15mL #2|Extraction Plate|100|Simple Transfer & Mix in-well x 10
2. Change tips
3. Repeat steps 1-2 for each column of plate with samples
4. Initiate magnet
5. Pause (Custom Adjust Time; Default = 15 mins)
6. Extraction Plate (pipette centered at bottom of well)|NEST 195mL Reservoir|200|Dispense & Blowout
7. Extraction Plate (pipette centered at bottom of well)|NEST 195mL Reservoir|200|Dispense & Blowout
8. Change tips
9. Repeat steps 6-7 for each column of plate with samples
10. NEST 15mL #1|Extraction Plate #1|200|Dispense & Blowout
11. NEST 15mL #1|Extraction Plate #1|200|Dispense & Blowout
12. Repeat steps 11-12 for each column of plate with samples
13. Pause (Custom Adjust Time; Default = 15 mins)
14. Extraction Plate #1|NEST 195mL Reservoir|200|Dispense
15. Extraction Plate #1|NEST 195mL Reservoir|200|Dispense & Blowout
16. Repeat steps 10-15 for each column of plate with samples
17. Pause (Custom Adjust Time; Default = 15 mins)
18. Deactivate Magnet
19. NEST 15mL #3|Extraction Plate #1|100|Dispense & Mix x 10
20. Change tips
21. Repeat 19-20 for each column of plate with samples
22. Pause (Custom Adjust Time; Default = 15 mins)
23. Initiate magnet
24. Pause (Custom Adjust Time; Default = 15 mins)

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
33e96a

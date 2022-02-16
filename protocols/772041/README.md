# Protocol Title (should match metadata of .py file)

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Partner Name](partner website link)

## Categories
* PCR
	* PCR Prep

## Description
This protocol distributes PCR mastermix from a source 96 deep well plate to a target Applied Biosystems Microamp optical 384 well 30 µL plate. The user can choose how many wells to transfer to (rounding up to the nearest number of columns) as well as how much volume to add to each well.

Explanation of parameters below:
* `Number of wells`: How many wells to transfer mastermix to on the target plate. This will be rounded up to the nearest number of full columns.
* `Volume of mastermix`: Volume of mastermix to add to each well (µL)
* `Reuse tips?`: Yes: Reuse tips when distributing the mastermix. No: Drop the tips after each distribution, and pick up new tips before each aspiration.

---

### Modules
* No modules

### Labware
* [Some 96 Deep well plate?](link to labware on shop.opentrons.com when applicable)
* [MicroAmp Optical 384-Well Reaction Plate](link to labware on shop.opentrons.com when applicable)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

### Pipettes
* [20 µL multi-channel pipette](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [20 µL filter tips](https://shop.opentrons.com/opentrons-20ul-filter-tips/)

### Reagents
* PCR mastermix in the first column of the source plate (well A1 to H1)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/772041/deck.jpg)

### Reagent Setup
* Source plate: slot 5
![Source plate](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/772041/source_plate.jpg)

---

### Protocol Steps
1. This section should consist of a numerical outline of the protocol steps, somewhat analogous to the steps outlined by the user in their custom protocol submission.
2. example step: Samples are transferred from the source tuberacks on slots 1-2 to the PCR plate on slot 3, down columns and then across rows.
3. example step: Waste is removed from each sample on the magnetic module, ensuring the bead pellets are not contacted by the pipette tips.

1. Pick up tips with the 20 µL multi-channel pipette
2. Aspirate the chosen volume of mastermix from the source plate
3. Distribute mastermix to the target plate
4. Drop the tips
4. Repeat steps 1 to 4 until the mastermix has been distributed to all wells  

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
protocol-hex-code

# 022548-2 - DNA extraction: Mastermix creation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Nucleic Acid Extraction & Purification
	* DNA Extraction

## Description
This protocol create a mastermix of binding buffer and bead mix. For large volumes the deck should use a NEST 12 well reservoir, and for smaller volumes a tuberack may be used as source and target for mastermix creation.

Designate the wells used for binding buffer and bead mix and the mastermix is created starting in the well or tube immediately after, and uses as many wells as required for creating mastermix for the indicated number of samples. The protocol creates a dead volume in addition to the 'active' volume of mastermix (100 uL for tubes, 1 mL for reservoirs) - this is to avoid the pipette aspirating air during mastermix dispension in part 2 of the protocol.

The protocol will create a maximum volume of 9.65 mL per tube or well, of which part is the dead volume.

The protocol is written to account for the changing liquid level of both source and target tubes so that the pipette will not plunge too far into tube solutions.

Explanation of parameters below:
* `Create mastermix for how many numbers of samples`: How many samples to create mastermix for.
* `Binding buffer wells`: Designates which wells or tubes contain binding buffer, you may specify a range such as 1-4, or a single number if it is a single tube/well. Numbering starts from Well/tube A1 and goes down the
* `Bead mix well(s)`: Which well(s) contain bead  mix. Just like the previous parameter it can be a number or a range, e.g. 5, or 5-6
* `Volume of binding buffer per source well (mL)`: How many milliliters of binding buffer is contained in each source tube/reservoir well.
* `Volume of bead mix per source well (mL)`: How many milliliters of bead mix is contained in each source tube/reservoir well
* `P300 single channel pipette mount`: Left or right mount
* `P300 multi channel pipette mount`: Left or right mount
* `Mastermix tuberack (Optional, only for small volumes of mastermix)`: Specify what kind of tuberack contains your source and destination tubes. If this parameter is set to none the mastermix source/target will be a NEST 12 well reservoir instead (default)
* `Mastermix mixing rate multiplier`: The multiplier scales the flow rate of mixing aspirations and dispenses, e.g. 1.0 is the standard mixing rate, 0.5 would be half etc.
* `Binding buffer aspiration flow rate multiplier`: Controls the flow rate of aspiration when aspirating binding buffer from a source well
* `Binding buffer dispensing flow rate multiplier`: Controls the flow rate of dispension when dispensing binding buffer in a mastermix target well
* `Bead solution aspiration flow rate multiplier`: Controls the flow rate of aspiration when aspirating from a bread mix source well
* `Bead solution dispensing flow rate multiplier`: Controls the flow rate of dispension when dispensing bead mix in a mastermix target well
* `How many times do you want to mix the mastermix?`: Indicates the number of times you want to mix the mastermix solution after the binding buffer and bead mix have been added.
* `Offsets from the tube edges for bead mix dispenses (mm)`: Offset defining how close the pipette may get to the edge of the tube when dispensing bead mix (which is dispensed in three different locations inside of the tube)
* `Offsets from the edges of the reservoir wells for bead mix dispenses (mm)`: Offset defining how close the pipette may get to the edge of the reservoir well when dispensing bead mix (which is dispensed in three different locations inside of the well)
* `Verbose protocol output?`: Indicates to the protocol whether it should output extra information about what it is doing.
---

### Modules
None required

### Labware
* [NEST 12-Well Reservoirs, 15 mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* [Opentrons tuberacks](https://shop.opentrons.com/4-in-1-tube-rack-set/)

### Pipettes
* [P300 multi-Channel (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [P300 single-Channel (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/022548/1/deck.jpg)

### Reagent Setup
* This is an example of what a reagent/target reservoir or tuberack setup may look like - binding buffer in the first four wells/tubes, bead mix in the fifth and then the next four wells are used to mix mastermix.

* Reservoir: slot 10
![reservoir](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/022548/1/resv.jpg)
* Tuberack: slot 10 alternative  
![tuberack](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/022548/1/tuberack.jpg)

---

### Protocol Steps
1. The binding buffer is distributed from the source wells to the target wells.
2. The bead mix is mixed ten times.
3. The bead mix is distributed from its source wells to its target wells.
4. The mastermix is mixed a number of times according to the parameter.

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
022548-1

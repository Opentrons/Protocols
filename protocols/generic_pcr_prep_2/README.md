# Generic PCR Prep Part 2 - Mastermix and DNA Distribution

### Author
[Opentrons](https://opentrons.com/)

## Categories
* PCR
    * Generic PCR Prep

## Description
Part 2 of 2: Master Mix Distribution and DNA Transfer

Links:
* [Part 1: Master Mix Assembly](./pcr_prep_part_1_gen2)
* [Part 2: Master Mix Distribution and DNA Transfer](./pcr_prep_part_2_gen2)


This protocol allows your robot to distribute a master mix solution from well A1 of a reservoir to a target (a plate or PCR strips). The robot will then transfer DNA samples to the master mix solution. The protocol works with both single- and multi-channel pipettes, just be sure that the minimum end of their combined volume range covers the smallest volume. There is also an option to place the DNA template labware, and the target labware on temperature modules to keep them cool.

Explanation of parameters below:
* `Number of samples` : The number of DNA template samples to mix with PCR mastermix on the target labware (e.g. a plate or tube strips on an aluminum block)
* `Right pipette type`: Pipette in the right mount, can be either a single channel or a multi-channel pipette
* `Left pipette type`: Pipette in the left mount, can be either a single channel or a multi-channel pipette.
* `Filtered or unfiltered tips for the left pipette?`: Whether the left pipette is using filter or regular tips
* `Filtered or unfiltered tips for the right pipette?`: Whether the right pipette is using filter or regular tips
* `Mastermix volume (in µl)`: The volume of mastermix for each well on the destination labware in microliters
* `DNA volume (in µl)`: The amount of DNA template to transfer to each destination well in microliters
* `Mastermix reservoir`: 12 well reservoir containing your PCR mastermix in well `A1`
* `PCR well plate (or PCR strips) containing template DNA`: Your source of template DNA, such as a 96 well plate
* `Destination PCR well plate or PCR strips`: This is the labware where DNA template and PCR mastermix is transferred and mixed
* `Temperature module for the template sample well plate`: (Optional) You can load a temperature module for your template plate if you want to control the temperature.
* `Temperature module for the destination well plate`: (Optional) You can load a temperature module for your destination plate if you want to control the temperature.

---

### Modules
* [12-channel reservoir](https://labware.opentrons.com/?category=reservoir)
* [96-well PCR plate]()
* [Alternatively: Well plate/PCR strips on aluminum blocks](https://labware.opentrons.com/?category=aluminumBlock)

### Pipettes
* [Single channel pipettes](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Pipette tips](https://shop.opentrons.com/universal-filter-tips/)

### Robot
* [OT-2](https://opentrons.com/ot-2)

---

### Deck Setup
* Example setup
![Deck](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/generic_pcr_prep_2/example_deck.jpg)


* Slot 1: Empty
* Slot 2: Empty
* Slot 3: 12-Channel reservoir: Well 1 - Mastermix source
* Slot 4: Tiprack 1 for the left pipette
* Slot 5: Tiprack 1 for the right pipette
* Slot 6: Destination plate (where mastermix and template DNA is combined)
* Slot 7: Tiprack 2 for the right pipette
* Slot 8: Tiprack 2 for the left pipette
* Slot 9: Template DNA plate
* Slot 10: Empty
* Slot 11: Empty


### Protocol Steps
1. Select your parameters.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. The robot will start by transferring mastermix to the destination labware.
9. The robot transfers DNA template samples to the destination plate

### Process
1. Input the number of samples you are processing.
2. Select your pipettes.
3. Input the desired master mix and DNA volume in each well.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will distribute master mix solution from trough to PCR strips in slot 2.
10. Robot will transfer DNA from PCR strips in slot 1 to those in slot 2.

Please reference our [Application Note](https://opentrons-protocol-library-website.s3.amazonaws.com/Technical+Notes/Thermocycler+PCR+Application+Note.pdf) for more information about the expected output of this protocol.

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
generic_pcr_prep_2

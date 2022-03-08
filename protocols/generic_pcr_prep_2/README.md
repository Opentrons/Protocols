# Generic PCR Prep Part 2 - Mastermix and DNA Distribution

### Author
[Opentrons](https://opentrons.com/)

## Categories
* PCR
    * Generic PCR Prep

## Description
Part 2 of 2: Master Mix Distribution and DNA Transfer

Links:
* [Part 1: Master Mix Assembly](./generic_pcr_prep_1)
* [Part 2: Master Mix Distribution and DNA Transfer](./generic_pcr_prep_2)


This protocol allows your robot to distribute a master mix solution from well A1 of a reservoir to a target (a plate or PCR strips). The robot will then transfer DNA samples to the master mix solution. The protocol works with both single- and multi-channel pipettes, just be sure that the minimum end of their combined volume range covers the smallest volume. There is also an option to place the DNA template labware, and the target labware on temperature modules to keep them cool. The protocol allows a user to transfer the samples of up to four 96 well plates to a 384 well plate if desired. The user can also control whether they want their DNA samples mixes, as well as the aspiration and dispensation flow rates of the pipettes.

Explanation of parameters below:
* `Number of samples` : The number of DNA template samples to mix with PCR mastermix on the target well plate. This parameter controls how many plate columns the mastermix is transferred to as well as how many columns of samples are transferred to the destination plate.
* `Number of mixes`: How many times to mix the samples with the mastermix after adding them together
* `Aspiration rate multiplier`: A multiplier for controlling the flow rate of aspiration, less than 1 to slow down, or greater than one to speed up.
* `Dispensation rate multiplier`: A multiplier for controlling the flow rate of dispensation, less than 1 to slow down, or greater than one to speed up.
* `Right pipette type`: Pipette in the right mount, can be either a single channel or a multi-channel pipette
* `Left pipette type`: Pipette in the left mount, can be either a single channel or a multi-channel pipette.
* `Filtered or unfiltered tips for the left pipette?`: Whether the left pipette is using filter or regular tips. for P20s and P10s the options are Opentrons 20 µL filtered tips, or 20 µL unfiltered.
for P50 and P300s the filtered tips are 200 µL Opentrons filtered tips, and the non-filtered are 300 µL Opentrons regular tips. For the P1000 the options is either Opentrons 1000 µL filtered or non-filtered tips.
* `Filtered or unfiltered tips for the right pipette?`: Whether the right pipette is using filter or regular tips
* `Mastermix volume (in µl)`: The volume of mastermix for each well on the destination labware (in µL)
* `DNA volume (in µl)`: The amount of DNA template to transfer to each destination well from each DNA template well (in µL)
* `Mastermix reservoir`: 1, or 12 well reservoir, or a deep well plate containing your PCR mastermix in well `A1` (or `A1` to `H1`)
* `PCR well plate (or PCR strips) containing template DNA`: Your source of template DNA, such as a 96 well plate (up to 4 when the destination plate is a 384 well plate)
* `Destination PCR well plate or PCR strips`: This is the well plate where the PCR mastermix and the  DNA template is transferred to and mixed.
* `Temperature module for the 1st DNA template well plate`: (Optional) You can load a temperature module for your (1st) DNA template well plate if you want to control its temperature.
* `Temperature module for the destination well plate`: (Optional) You can load a temperature module for your destination well plate if you want to control its temperature.


---
</br>

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Labware
* [Reservoir](https://labware.opentrons.com/?category=reservoir)
* [Deep Well plates](https://labware.opentrons.com/?category=wellPlate) may also be used as reservoirs
* [Well plates](https://labware.opentrons.com/?category=wellPlate)
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

![Mastermix Reservoir](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/generic_pcr_prep_2/mastermix_reservoir.jpg)


* Slot 1: Template DNA plate 2 (optional: for transferring to a 384 well plate)
* Slot 2: Template DNA plate 3 (optional: for transferring to a 384 well plate)
* Slot 3: Reservoir: or Deep well plate: Well 1 (to 8)- Mastermix source
* Slot 4: Tiprack 1 for the left pipette
* Slot 5: Tiprack 1 for the right pipette
* Slot 6: Destination plate (where mastermix and template DNA is combined, optionally on a temperature module)
* Slot 7: Tiprack 2 for the right pipette
* Slot 8: Tiprack 2 for the left pipette
* Slot 9: Template DNA plate 1 (optionally on a temperature module)
* Slot 10: Empty
* Slot 11: Template DNA plate 4 (optional: for transferring to a 384 well plate)


### Protocol Steps
1. The protocol distributes mastermix to the destination plate
3. DNA template samples are transferred from the DNA source plates to the destination plate
4. The samples are mixed by pipetting

### Process
1. Input the parameters you wish to control.
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

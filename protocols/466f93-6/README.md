# 466f93-6 - Mastermix creation protocol

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
	* Mastermix creation

## Description
This protocol lets you create mastermixes for end repair, adaptor ligation and PCR mastermix (PCR mix + primers) transferring reagents from the yourgene_reagent_plate_I plate to a tuberack of your choice.

End repair mastermix will be created in well A1, adaptor ligation: A2, PCR mastermix: A3 (i.e. down the column of the tuberack)

Explanation of parameters below:
* `Number of samples`: The number of samples that you wish to create mastermix for
* `Number of over-reactions`: How many extra reaction volumes to create in each mastermix tube in order to have an excess volume to account for pipetting errors and low well volumes that may be difficult for the pipette to aspirate.
* `Aspiration rate multiplier`: 1.0 is regular aspiration flow rate, anything less would slow it down, and increasing it beyond 1.0 would speed it up.
* `Dispensing rate multiplier`: 1.0 is regular dispensing flow rate, anything less would slow it down, and increasing it beyond 1.0 would speed it up.
* `Mixing rate multiplier`: Rate multiplier for mixing, affects both aspiration and dispensing flow rate for mixes.
* `Number of mixes`: How many times you would like mastermixes to be mixed after creation.
* `Left pipette mount`: Which pipette (if any) to mount in the left mount.
* `Use filter tips with the left pipette?`: Choose whether to use regular or filter tips with the left pipette.
* `Right pipette mount`: Which pipette (if any) to mount in the right mount.
* `Use filter tips with the right pipette?`: Choose whether to use regular or filter tips with the right pipette.
* `Create end-repair mastermix?`: Choose whether to create end repair buffer/enzyme mastermix.
* `Create adaptor ligation mastermix?`: Choose whether to create adaptor ligation buffer/enzyme mastermix.
* `Create PCR reaction mastermix?`: Choose whether to create PCR reaction mastermix. This function mixes the PCR mastermix with primers.
* `Mastermix target labware`: What kind of labware you would like to create the mastermix in? Make sure to select the aluminum option if you are using a temperature module.
* `Do you want verbose output from the protocol?`: If set to 'Yes' the protocol will report additional information about what it is doing.
* `Temperature module for the reagent plate?`: Use a temperature module for the reagent plate. The reagent plate must be loaded onto the aluminum block.
* `Temperature module for the mastermix target tuberack?`: Use a temperature module for the tuberack where mastermixes are created. The tuberack must be loaded onto the temperature module with an aluminum block.
* `Set temperature for temp. modules`: The temperature to hold the temperature modules at (in degrees Celcius)

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Labware
* [Opentrons tuberacks](https://shop.opentrons.com/4-in-1-tube-rack-set/)

### Pipettes
* [Single-Channel pipette(s) (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/466f93-6/deck.jpg)

1. Empty
2. Empty
3. Empty
4. Mastermix destination - Tuberack on optional temperature module
5. Tiprack for the left pipette
6. Empty
7. Yourgene Reagent Plate I on optional temperature module
8. Tiprack for the right pipette
9. Empty
10. Empty
11. Empty
12. Empty


---

### Protocol Steps
1. For each mastermix creation routine that is selected the protocol will:
2. Transfer the reagents to the tuberack
3. Mix the newly created mastermix as many times as specified by the `Number of mixes` parameter

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
466f93-6

# Protocol Title (should match metadata of .py file)

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Partner Name](partner website link)

## Categories
* NGS Library Prep
	* Mastermix creation

## Description
This protocol lets you create mastermixes for end repair, adaptor ligation and PCR mastermix (PCR mix + primers) transferring reagents from the yourgene_reagent_plate_I plate to a tuberack of your choice.

Explanation of parameters below:
* `Number of samples`: The number of samples that you wish to create mastermix for
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
* `Mastermix target labware`: What kind of labware you would like to mix the mastermix in.
* `Do you want verbose output from the protocol?`: If set to 'Yes' the protocol will report additional information about what it is doing.
---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Labware
* [Opentrons tuberacks](https://shop.opentrons.com/4-in-1-tube-rack-set/)

### Pipettes
* [Single-Channel pipette(s) (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup
* If the deck layout of a particular protocol is more or less static, it is often helpful to attach a preview of the deck layout, most descriptively generated with Labware Creator. Example:
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

### Reagent Setup
* This section can contain finer detail and images describing reagent volumes and positioning in their respective labware. Examples:
* Reservoir 1: slot 5
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res1_v2.png)
* Reservoir 2: slot 2  
![reservoir 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res2.png)

---

### Protocol Steps
1. This section should consist of a numerical outline of the protocol steps, somewhat analogous to the steps outlined by the user in their custom protocol submission.
2. example step: Samples are transferred from the source tuberacks on slots 1-2 to the PCR plate on slot 3, down columns and then across rows.
3. example step: Waste is removed from each sample on the magnetic module, ensuring the bead pellets are not contacted by the pipette tips.

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

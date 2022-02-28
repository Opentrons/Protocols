# Protocol Title (should match metadata of .py file)

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Partner Name](partner website link)

## Categories
* Sample prep
	* Microscopy slide antibody staining

## Description
This protocol performs immunostaining of slides in a custom 3D printed slide holder with Shandon coverplates.
Up to 7 slide holders, each with 8 wells can be placed on the deck resulting in the ability to stain up to 56 slides simultaneously.

Explanation of parameters below:
* `Number of slide blocks`: How many slide holding blocks there are on the deck  
* `Volume in reagents containers`: How much volume there is in each reagent container (meaning block, antibody 1, antibody 2, and nuclear counterstain)
* `Do step x`:
* `Reagent tuberack`: What type of tuberack you wish to use
* `Pipette offset`: Pipetting offset in mm when dispensing, increasing this parameter will mean that the pipette will dispense at a lower height in the wells
* `Do a dry run?`: Skip pauses and return tips to their racks after use

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Labware
* [Opentrons tuberacks](https://shop.opentrons.com/4-in-1-tube-rack-set/)
* [Agilent 1-Well Reservoir 290 mL](https://labware.opentrons.com/agilent_1_reservoir_290ml)'

### Pipettes
* [P300 single-Channel (GEN2)}](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P1000 single-Channel (GEN2)}](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

### Reagents
* Block
* Antibody 1
* Antibody 2
* Nuclear counterstain

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

# Protocol Title (should match metadata of .py file)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* PCR
    * Generic Mastermix Assembly

## Description
Part 1 of 2: Master Mix Assembly

This protocol allows your robot to create a master mix solution using any reagents stored in one or two different pieces of labware such as a tube racks or well plates. The master mix will be created in well A1 of the trough of the chosen reservoir. The ingredient information will be provided as a CSV file. See Additional Notes for more details.

Links:
* [Part 1: Master Mix Assembly](./pcr_prep_part_1_gen2)
* [Part 2: Master Mix Distribution and DNA Transfer](./pcr_prep_part_2_gen2)


Explanation of parameters below:
* `right pipette type`: Pipette for the right mount
* `Left pipette type`: Pipette for the left mount
For the pipette choices it is important that the pipettes selected will cover the range of volumes used in the protocol
* `master mix .csv file`: Here, you should upload a .csv file formatted in the following way, being sure to include the header line:
![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1473-acies-bio/CSV.png)

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Thermocycler Module](https://shop.opentrons.com/collections/hardware-modules/products/thermocycler-module)
* [HEPA Module](https://shop.opentrons.com/collections/hardware-modules/products/hepa-module)

### Labware
* [Labware name](link to labware on shop.opentrons.com when applicable)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

### Pipettes
* [Pipette name](link to pipette on shop.opentrons.com)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

### Reagents
* [kit name when applicable](link to kit)
* Nick is working on auto-filling these sections from the protocol (3/28/2021)

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

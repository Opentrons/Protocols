# Fetal DNA NGS library preparation part 5 - LifeCell NIPT 35Plex HV - Normalization

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep

## Description
This protocol uses a CSV file (as described) below to normalize DNA samples based on their concentration. After normalization all normalized samples will have a volume of 10 µL and have the same concentration as the least concentrated input sample.

* `Number of samples`: The number of DNA samples on your sample plate. Should be between 7 and 36.

Explanation of complex parameters below:
* `Sample concentration Input CSV File`: Upload a CSV file with the formatting shown in the block below that specifies the concentration of the sample (ng/µL). Note: The units are arbitrary provided that they are the same for all samples.

**Example**
```
well,concentration
1,3.6
2,3.63
3,5.86
```

---

### Labware
* [Bio-Rad 96 well 200 µL PCR plate](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr?category=wellPlate)

### Pipettes
* [P300 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P20 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [Opentrons 96 Filter Tip Rack 20 µL](https://labware.opentrons.com/opentrons_96_filtertiprack_20ul/)
* [Opentrons 96 Filter Tip Rack 200 µL](https://labware.opentrons.com/opentrons_96_filtertiprack_200ul/)

---

### Deck Setup

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/466f93/deck_state_part5_466f93.jpeg)

![reservoir layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/466f93/reservoir_layout_466f93_part4.jpeg)

### Reagent Setup
* Slot 1 Plate with Qubit HS quantified samples (DP-5 from part 4)
* Slot 2 Empty
* Slot 3 Empty
* Slot 4 Destination Plate 6 - Normalization plate
* Slot 5 200 µL Opentrons filter tips
* Slot 6 12-well reservoir (Well 2: water (>2 mL))
* Slot 7 Empty
* Slot 8 Empty
* Slot 9 Empty
* Slot 10 20 µL Opentrons filter tips
* Slot 11 20 µL Opentrons filter tips

---

### Protocol Steps
1. The user places all the required labware on the deck and makes sure to replace any used or partially used tip racks
2. The protocol reads the CSV (describe above) and determines which samples has the lowest concentration of DNA according to the CSV inputs.
3. Each sample is transferred to DP-6 on Slot 4 and is mixed with water such that all concentrations will be the same as that of the least concentrated sample and the total volume is 10 µL. Note that the p20 is not designed to transfer volumes < 1 µL. Therefore please ensure that there is no sample which differs more than 10:1 in concentration with any other sample.


### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
466f93-5

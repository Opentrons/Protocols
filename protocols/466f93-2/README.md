# Fetal DNA NGS library preparation part 2 - LifeCell NIPT 35Plex HV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Next Generation Sequencing (NGS)

## Description
This protocol mixes end-repaired DNA samples with adaptor ligation mastermix and DNA barcodes specified according to a CSV input file

Explanation of complex parameters below:
* `Sample:Barcode Input CSV File`: Upload a CSV file with the formatting shown in the block below that specifies which sample is mixed with which barcode and the barcode's identifier:

```
Sample ID,Slot number ,Rack position,Wellplate A position,Wellplate A well position
Sample1,1,1,3,A1
Sample2,1,2,3,A2
Sample3,1,3,3,A3
```

* `Sample Volume`: The amount of sample to transfer from the tubes to the plate.
* `Acetonitrile Transfer`: Whether to transfer acetonitrile into the plates (Steps 6-8).
* `P300 Single Channel GEN2 Mount Position`: Select the pipette mount position.
* `P300 Multi Channel GEN2 Mount Position`: Select the pipette mount position.
* `Blowout After Dispensing Sample`: Whether to blow out after dispensing sample.
* `Sample Aspiration Flow Rate (uL/s)`: The flow rate when aspirating liquid.
* `Sample Dispense Flow Rate (uL/s)`: The flow rate when dispensing liquid for both the samples and MeCN.
* `Use temperature module`: Specify whether to use the temperature module on slots 3 and 6 with mounted deepwell plates. Note: if using the temperature modules, they should be placed in slots 3, and 6 respectively, in that order depending on running 1 or 2 plates.

---

### Labware
* TBD

### Pipettes
* [P300 Single Channel GEN2](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette?variant=5984549109789)
* [P300 Multi Channel GEN2](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette?variant=5984202489885)

---

### Deck Setup

**One Plate Example:**

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/459cc2/459cc2-layout.png)

### Reagent Setup
* Slot 7 Reservoir: Acetonitrile

---

### Protocol Steps
1. Aspirate 50 uL of the sample from tube rack using the single channel pippete P300. Add a 20 uL air gap.					
2. Dispense sample into a A1 of Plate 1. Use blowout after dispensing. (Repeat for same well on Plate 2 if needed).
3. Discard tip into the trash bin.
4. Repeat steps 1-3 for all wells in the CSV file.
5. Pick up tips with the multichannel pipette, transfer 100 uL of Acetonitrile to all wells in the plate.
6. Discard tip into the trashbin.

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
459cc2

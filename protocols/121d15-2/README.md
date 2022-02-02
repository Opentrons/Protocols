# HPLC Picking

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Plate Filling

## Description

Links:
* [Manual Cleave](./121d15)
* [HPLC Picking](./121d15-2)

This protocol performs a custom HPLC Picking protocol from a worklist. The worklist should be specified as follows:

```
Number of Redo
8
pos TB_RCK_1,pos MTP_1,vol
1,1,200
2,135,200
3,2,150
4,100
5,84
6,262
7,242
8,218
...
```

---

### Labware
* Custom 48-tuberack
* [Greiner MASTERBLOCK 384 Well Plate 225 µL](https://shop.gbo.com/en/row/products/bioscience/microplates/polypropylene-storage-plates/384-deep-well-masterblock/781270.html)
* [Greiner MASTERBLOCK 96 Well Plate 500 µL](https://shop.gbo.com/en/row/products/bioscience/microplates/polypropylene-storage-plates/96-well-masterblock-0-5ml/786201.html)
* [Opentrons 300µL Tips](https://shop.opentrons.com/opentrons-300ul-tips-1000-refills/)

### Pipettes
* [P300 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/121d15/deck.png)

---

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
121d15

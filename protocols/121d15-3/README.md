# HPLC Picking

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description

Links:
* [Manual Cleave](./121d15)
* [Redo Replacement Picking](./121d15-2)
* [HPLC Picking](./121d15-3)

This protocol performs a custom HPLC Picking protocol from a worklist. The worklist should be specified as follows:

```
well1,well2,well3,well4,tube,vol
1,100,200,300,A1,200
2,101,201,301,B1,200
3,102,202,302,C1,200
4,103,203,303,D1
5,104,204,304,E1,100
6,105,205,305,F1
...
```

---

### Labware
* [Irish Life Sciences 2.2mL Deep Well Plate, V-Bottom #2.2S96-008V](https://irishlifesciences.com/product/2-2ml-96well-square-well-pyramid-bottoms)
* [Opentrons 300µL Tips](https://shop.opentrons.com/opentrons-300ul-tips-1000-refills/)

### Pipettes
* [P300 Single Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/121d15/deck3.png)

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

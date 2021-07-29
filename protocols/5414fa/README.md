# Vitrolife Plate Prep

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Plate Filling

## Description
This protocol performs the preparation of media and oils onto the [Vitrolife Micro-droplet Culture Dish](https://www.vitrolife.com/products/labware/dishes/). It adds media to each of the 12 wells in the plate by distributing 20 uL in a single take. It will then transfer a total of 5 mL of oil to the inner perimeter of the plate. **This protocol is still a Work In Progress and is subject to refactoring based on a pending custom labware piece.**

---

### Labware
* [Opentrons 200 uL Filter Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-200ul-filter-tips)
* [Opentrons 1000 uL Filter Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-filter-tips)
* [Vitrolife Micro-droplet Culture Dish](https://www.vitrolife.com/products/labware/dishes/)

### Pipettes
* [P300 Single GEN2 Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette?variant=5984549109789)
* [P1000 Single GEN2 Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette?variant=5984549142557)

### Reagents
* [Global Total Media](https://fertility.coopersurgical.com/art_media/global-total/)
* [Life Global LifeGuard Oil](https://fertility.coopersurgical.com/art_media/lifeglobal-oils/)

---

### Deck Setup
**Deck Setup is currently unavailable as the custom labware component to house the plates and reagents on the OT-2 deck are actively being developed.**

The protocol currently uses a dummy labware definition of the Vitrolife dish to display the basic protocol logic using our Python API. 
![Vitrolife Dish](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5414fa/vitrolife_culture_dish.png)

---

### Protocol Steps
1. Distribute 20 uL of media on each well of plate 1 in the following order: A1, A2, A3, A4, B4, B3, B2, B1, C1, C2, C3, C4.
2. Aspirate 1000 uL of oil and dispense it onto plate 1. (Repeat Step 4 more times).
3. Repeat steps 1 and 2 for all plates on deck.

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
5414fa
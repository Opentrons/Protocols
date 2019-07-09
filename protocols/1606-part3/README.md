# Cell Culture Assay Part 3: Fluorescence Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
This protocol performs cell culture assay part 3 of 3, which performs fluorescence preparation by first diluting cultures from a source 24-well culture plate to a fresh 24-well plate, and then transferring these diluted cultures in replicates to a black 96-well microtiter plate. Culture locations from part 1 are specified in the first CSV file; destinations for replicates on the 96-well microtiter plate are specified in the second CSV file; volumes (in ml) to dilute cultures from the 24-well source plate to a fresh 24-well plate are specified in the third CSV.

---

Links:
* [Part 1: Overnight Culture Prep](./1606-part1)
* [Part 2: OD Calculation](./1606-part2)

---

You will need:
* [Greiner Bio-One black microtiter plate # 655900](https://ecatalog.corning.com/life-sciences/b2c/EUOther/en/Permeable-Supports/Inserts/Corning%C2%AE-96-well-Clear-Polystyrene-Microplates/p/3370)
* [Corning Costar 24-well clear TC-treated culture plate](https://ecatalog.corning.com/life-sciences/b2c/UK/en/Microplates/Assay-Microplates/96-Well-Microplates/Costar%C2%AE-Multiple-Well-Cell-Culture-Plates/p/3526)
* [Axygen single well high profile single-channel reservoir](https://www.fishersci.se/shop/products/axygen-single-well-high-profile-reagent-reservoirs-8/11360275)
* [Opentrons P1000 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [1000ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV files.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
pLM5O2bm
1606

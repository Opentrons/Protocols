# Cell Culture Assay Part 1: Overnight Culture Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
This protocol performs cell culture assay part 1 of 3, which performs media addition to 24-well plate wells specified via CSV.

---

Links:
* [Part 2: OD Calculation](./1606-part2)
* [Part 3: Fluorescence Preparation](./1606-part3)

---

You will need:
* [Corning Costar 24-well clear TC-treated culture plate](https://ecatalog.corning.com/life-sciences/b2c/UK/en/Microplates/Assay-Microplates/96-Well-Microplates/Costar%C2%AE-Multiple-Well-Cell-Culture-Plates/p/3526)
* [Axygen single well high profile single-channel reservoir](https://www.fishersci.se/shop/products/axygen-single-well-high-profile-reagent-reservoirs-8/11360275)
* [Opentrons P1000 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [1000ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV file and select the mount for your P1000 pipette.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 1ml of media is transferred to each specified well of the the 24-well plate.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
pLM5O2bm  
1606

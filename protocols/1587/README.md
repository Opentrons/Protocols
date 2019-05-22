# CSV Tip Cherrypicking

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol performs tip cherrypicking from source to target plates as specified in an input CSV file. If specified, the tip is transferred to the next available well in the destination rack, moving down the rack columns before across the rack rows. The number of input racks and fresh empty racks to load are automatically determined through parsing the input CSV file.

---

You will need:
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV and select your pipette mount side.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Specified tips are transferred to the next available well in the empty tip racks.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
NIU0CiVq  
1587

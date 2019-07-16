# CSV Consolidation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol allows the robot to create up to 4 different pooling samples by consolidating cherrypicked wells from a 96 tall-well plates. The user will need upload one CSV each for increase, no change, decrease, and inactive property changes. Each CSV will contain information of the wells from which to be picked. See Additional Notes for the format of the CSVs, as well as the arrangement of pooling tubes in the Opentrons 4x6 2ml Eppendorf tuberack. If you would like to skip a pool as specified by 1 of the 4 CSV files, upload an empty CSV file corresponding to that pool.

---

You will need:
* [Opentrons 2ml Eppendorf Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Opentrons P50 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons 300ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV files, input the volume of each mutant to transfer, select the pipette mount, and select the tip use strategy.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Up to 4 pools are created based on the source wells specified in the corresponding CSV file.

### Additional Notes
Your CSV files should contain source wells of the 96-well source plate each on its own line, as in the following:  
```
A2
A3
A4
A7
A8
B3
B5
```

The pooling tubes are seated in the Opentrons tube rack according to the following setup:
* inactive: tube A1
* decrease: tube B1
* no change: tube C1
* increase: tube D1

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
66aa48

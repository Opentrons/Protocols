# 24- to 96-Well Plate Consolidation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Mapping

## Description
This protocol plate consolidation from 4 24-well deep plates to 1 96-well deep plate. The protocol allows the user to input the transfer volume for the process, which will necessitate the use of either the P10 (volume < 30ul) or P300 (volume >= 30ul) multi-channel electronic pipette. Please note that in order for the multi-channel pipette to avoid crashing in to the labware, every other row of both tip racks used in this experiment must be removed--only wells in rows A, C, E, and G will be occupied by tips.

---

You will need:
* [USA Scientific 96-Well Deep Plate](https://www.usascientific.com/2ml-deep96-well-plateone-sterile.aspx)
* [EnzyScreen 24-Well Deep Plate](https://www.enzyscreen.com/microplates_24_well_mtps.htm)
* [P10 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [P300 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Select transfer volume (ul).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The multi channel pipette will pick up tips on channels 1, 3, 5, and 7 to accommodate the larger 4-well columns of the 24-well plate.
8. The selected transfer volume is transferred from column 1 (A1, B1, C1, D1) of the first 24-well plate to wells A1, C1, E1, and G1 of the 96-well plate. The tips are discarded.
9. This process continues across the first and second 24-well plate to wells A2, C2, E2, and G2 until rows A, C, E, and G of the 96-well plate are filled.
10. Step 8 is repeated from the third 24-well plate to wells B1, D1, F1, and H1 of the 96-well plate.
11. Step 10 is repeated across the third and fourth 24-wells plates until rows B, D, F and H of the 96-well plate are filled.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
YFRrGTb4  
1561

# Cell Culture Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
With this protocol, you can perform a 10x serial dilution using buffer from a 12-row trough reservoir for up to 12 samples, setup according to the diagram in the Additional Notes section below. Each sample is diluted 8 times, but only the 6 most dilute samples are transferred to the Petri dishes. The samples are then distributed to one (up to 6 samples) or two (up to 12 samples) Petri dishes according to the schematic in the Additional Notes section below.

Note: Please calibrate the Petri dishes such that the pipette tip barely touches the gel.

---

You will need:
* [12-row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons 4x6 2ml tube rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [VWR 96-well culture plate](https://us.vwr.com/store/catalog/product.jsp?catalog_number=10861-562)
* [VWR Square Petri dish](https://us.vwr.com/store/catalog/product.jsp?catalog_number=82051-068)
* [Opentrons 300ul tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 10ul tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P50 8-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Select the number of samples you will be running (maximum 12 samples).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The p50 multi-channel pipette distributes 90ul from row 1 of the 12-row trough to each row of the 96-well plate using the same tips.
8. The p10 single-channel pipette transfers 10ul of sample 1 to row A column 1 of the plate.
9. Step 8 is repeated for each sample across row A of the plate for up to 12 samples.
10. A 10x serial dilution is performed for the sample in row A column 1: for each column, the 0.1 concentration (10ul sample in 90ul buffer) is mixed, and 10ul is transferred into the well below. This is repeated until the dilution reaches row H, where the contents are mixed and 10ul are transferred to the liquid trash in row 12 of the 12-row trough for volume consistency down the dilution series.
11. Step 10 is repeated for each sample across row A of the plate for up to 12 samples. Each sample's dilution uses the same tip, and the tip is refreshed between sample dilutions.
12. Column 1 rows C-H (6 most dilute dilutions in the sample dilution series) are transferred to the the corresponding row in the Petri dish according to the schematic in Additional Notes below. The most dilute (row H) is transferred to the 1st well of the Petri dish row. The second most dilute (row G) is transferred to the 2nd well, and so on, until the least dilute (row C) is transferred to the 6th well in the row.
13. Step 12 is repeated for each sample across the columns of the plate. If there are more than 6 samples selected, the sample 7 transfers move to the 1st row of the 2nd plate, and further samples continue down the rows of the 2nd plate. The same tip is used for each sample (6 transfers), and the tip is refreshed between transfers.

### Additional Notes
![Tube Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1544-smartphage-inc-dba-fayeface/tube_setup.png)  

![Liquid Transfer Schematic](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1544-smartphage-inc-dba-fayeface/petri_dish_transfer_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
3kSBYo4S  
1544

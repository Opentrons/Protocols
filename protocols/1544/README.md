# Cell Culture Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
With this protocol, you can perform a cell assay distribution to 4 Petri dishes from 2 plates of samples (2 dishes to one sample plate) according to the schematic in the Additional Notes section below.

---

You will need:
* [Opentrons 4x6 2ml tube rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [VWR 96-well culture plate](https://us.vwr.com/store/catalog/product.jsp?catalog_number=10861-562)
* [VWR Square Petri dish](https://us.vwr.com/store/catalog/product.jsp?catalog_number=82051-068)
* [Opentrons 10ul tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Column 1 rows C-H of the first sample plate (6 most dilute dilutions in the sample dilution series) are transferred to the the corresponding row in the Petri dish according to the schematic in Additional Notes below. The most dilute (row H) is transferred to the 1st well of the Petri dish row. The second most dilute (row G) is transferred to the 2nd well, and so on, until the least dilute (row C) is transferred to the 6th well in the row.
7. Step 6 is repeated for each sample across the columns of the plate. Samples 7 of the first plate are transferred to to the 1st row of the 2nd dish, and samples 8-12 continue down the rows of the 2nd plate. The same tip is used for each sample (6 transfers), and the tip is refreshed between transfers.
8. Steps 6-7 are repeated for the second plate and other 2 Petri dishes.

### Additional Notes
![Liquid Transfer Schematic](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1544-smartphage-inc-dba-fayeface/petri_dish_transfer_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
3kSBYo4S  
1544

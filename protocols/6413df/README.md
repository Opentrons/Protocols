# Cherrypicking: Plasmid Transfection

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol allows your robot to cherrypick plasmids for 3 transfections. 96-96 plasmids are placed in the Matrix 2D Barcoded Storage Tubes. The source reagents and final transfection tubes are in 50 mL centrifuge tubes and are placed in separate 50 mL tube racks. User can define the transfections by uploading a CSV. See the required format of the CSV and the reagent setup in Additional Notes below.

---

You will need:
* [Opentrons 1000 µL Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 10/50/300 µL Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Thermo Scientific™ Matrix™ 2D Barcoded Open-Top Storage Tubes 1.4 mL](https://www.thermofisher.com/order/catalog/product/3792?SID=srch-hj-3792)
* [Corning™ Mini Bioreactor Centrifuge Tube 50 mL](https://www.fishersci.com/shop/products/corning-mini-bioreactor-centrifuge-tube-50ml/07202150)
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)

### Robot
* [OT-2](https://opentrons.com/ot-2)


## Process
1. Select your single-channel pipette on the right mount.
2. Upload your cherrypicking CSV.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will transfer Reagent 1 from Source Tubes well A1 to all wells in Final tubes.
9. Robot will transfer plasmids based on the CSV input to wells A1-A3 in Final Tubes.
10. Reagent 2 from Source Tubes well A2 will then be added and mixed in wells B1-B3 of Final Tubes.
11. After 4.5 minutes of incubation, the entire contents (1500 µL) of B1-B3 will be transferred to A1-A3 respectively.


### Additional Notes
Reagent Setup:

![reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/6413df/reagent_setup.png)

---

CSV Setup:

![csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/6413df/csv_setup.png)
* Keep the header
* Each row represents a transfection and corresponds to each column in the 50 mL tube rack, i.e. row 1: well A1 and B1; row 2: well A2 and B2; row 3: well A3 and B3
* Put "N/A" for plasmids and plasmid volume if fewer than 4 plasmids are needed in a transfection

---


If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
6413df

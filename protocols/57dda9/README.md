# Cell Culture Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
This protocol performs a cell culture assay in 3 parts:
1. media aliquoting from a reservoir to 4 24-deepwell plates
2. serial dilution across each deepwell plate
3. cell treatment from deepwell plates to 4 96-well plates (round or flat, upon user selection)

For specific deck setup and transfer scheme, please see 'Additional Notes' below.

---

You will need:
* [Greiner CELLSTAR 96-well plates round bottom # 650180](https://www.sigmaaldrich.com/catalog/product/sigma/m9436?lang=it®ion=IT)
* [Falcon 96-well Clear Flat Bottom TC-treated Culture Microplate # 353072](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Falcon%C2%AE-96-well-Polystyrene-Microplates/p/353072)
* [Axygen 24-Deep well plates # P-DW10ML24C](https://ecatalog.corning.com/life-sciences/b2c/US/en/Genomics-&-Molecular-Biology/Automation-Consumables/Deep-Well-Plate/Axygen%C2%AE-Deep-Well-and-Assay-Plates/p/P-DW-10ML-24-C)
* [BRAND 6-well trough pyramid bottom # BRND701456](https://it.vwr.com/store/product/14448281/reagent-reservoirs-for-multi-channel-pipettes-and-automatic-systems)
* [Opentrons P1000 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons P300 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 1000ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [Opentrons 300ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
Deck Scheme:  
![deck scheme](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/57dda9/deck_scheme.png)

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
57dda9

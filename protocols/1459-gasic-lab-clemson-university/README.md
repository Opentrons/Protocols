# General KASP Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
With this protocol, your robot can perform basic KASP protocol on up to 96 samples with up to 7 master mixes.

---

You will need:
* P10 Single-channel Pipette
* P10 Multi-channel Pipette
* [PCR Plates, 96-well, Semi-skirted](https://www.thermofisher.com/order/catalog/product/AB1400L)
* [PCR Racks](https://www.fishersci.com/shop/products/fisherbrand-96-well-pcr-racks-6/p-4272191)
* 10 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Set the number of master mixes and samples you are processing.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 4 uL of each column of DNA sample plate (slot 1) to the corresponding column of each output plates using the multi-channel pipette.
8. Robot will transfer 4 uL of each master mix to each plate using the single-channel pipette.


### Additional Notes
* DNA Sample Plate: Slot 1
* Output Plates: Slot 2, 3, 5, 6, 8, 9, and 11

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ifTF5MDp
1459

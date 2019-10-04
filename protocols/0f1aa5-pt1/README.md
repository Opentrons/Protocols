# Cell Culture Assay: Part 1

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
This protocol performs part 1/6 of a custom cell culture assay protocol.

---

You will need:
* Fisherbrand 24-vial rack
* USA Scientific 96-deepwell plate 2.4ml
* USA Scientific 12-channel reservoir
* [Opentrons P10 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [Opentrons P300 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* Opentrons 4-in-1 tuberack with 1.5ml snapcap tubes
* Fisherbrand 10ul/300ul Tips

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* [MagMAX DNA Multi-Sample Ultra Kit # A25597](https://www.thermofisher.com/order/catalog/product/A25597)
* Nuclease-free H2O

## Process
1. Upload your CSV file, input your pipette mounts, and select the magnet setup for your elution plate.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
6x15ml 4x50ml tuberack setup:
* media: well A3

1.5ml tuberack setup:
* L: well A1
* D: well B1
* DM: well C1
* NS: well D1
* HPS: well A2

Reagent trough setup:
* CTG: channel 1
* PBS: channels 2-3
* media: channel 4
* MGS: channel 5
* HPR: channel 6

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
0f1aa5

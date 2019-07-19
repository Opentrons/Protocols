# DNA Dilution from CSV

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
This protocol performs DNA dilutions on custom 96-well elution and dilution plates. The elution plate is mounted on a magnetic deck to separate beads. Transfer volumes are specified by a CSV file that can be uploaded on the custom protocol site. For reagent setup, see Additional Notes below.

---

You will need:
* [Thermo Fisher Scientific KingFisher 96 plate 200uL # 97002540](https://www.thermofisher.com/order/catalog/product/95040450)
* [USA Scientific TempPlate 96-well full skirt 0.1mL PCR plates # 1402-9800](https://www.usascientific.com/full-skirted-96-well-PCR-plate.aspx)
* [USA Scientific Channelmate 25ml reservoir # 1306-2590](https://www.usascientific.com/channelmate.aspx)
* [Opentrons P10 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P50 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [Opentrons 10ul Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300ul Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

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
7. The magnetic deck engages, and the protocol delays 2 minutes for the elution plate contents with beads to incubate on the magnet.
8. The specified volumes of nuclease-free H2O is transferred to each well of the OA dilution plate using the same tip. The pipette type is automatically selected based on transfer volume.
9. The specified volumes of elution plate solution are transferred to their corresponding wells on the OA dilution plate using a new tip for each transfer. The pipette type is automatically selected based on the transfer volume.
10. The specified volumes of nuclease-free H2O is transferred to each well of the CNV dilution plate using the same tip. The pipette type is automatically selected based on transfer volume.
11. The specified volumes of OA plate contents are transferred to their corresponding wells on the CNV dilution plate using a new tip for each transfer. The pipette type is automatically selected based on the transfer volume.

### Additional Notes
Reagent trough setup:  
* nuclease-free H2O: channel 1

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ya76sE6P  
1610

# Cell Culture Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
This protocol performs a cell culture assay on up to 8 culture plates using 2 P300 multi-channel pipettes.

---

You will need:
* [Corning 96-well plates 360ul, flat # 3598](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Corning%C2%AE-96-well-Solid-Black-and-White-Polystyrene-Microplates/p/corning96WellSolidBlackAndWhitePolystyreneMicroplates)
* Sorenson 1-channel reservoirs 200ml, v-bottom # 74030
* [Opentrons P300 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 300ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons magnetic module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

## Process
1. Input the number of plates that will be processed.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The left P300 multi pipette aspirates 100ul from columns 1-3 of plate 1, and the right P300 multi pipette aspirates 100ul from columns 4-6 of plate 1. Each pipette blows out in the waste reservoir.
8. Step 8 repeats for columns 4-6 and 10-12, respectively.
9. Steps 7 and 8 are repeated for all plates specified. The same tips are used for all media removals and dropped after the last removal.
10. The left and right pipettes aspirate 300ul from the fresh media reservoir. The left pipette distributes 100ul to columns 1-3 of plate 1, and the right pipette distributes 100ul to columns 4-6 of plate 1. Any excess fresh media is blown out into the waste reservoir.
11. Step 10 is repeated for columns 4-6 and 10-12, respectively.
12. Steps 10 and 11 are repeated for all plates specified. The same tips are used for all fresh media distributions and dropped after the last distribution.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
8249aa

# NGS CSV Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library preparation through pooling source wells in 1.5ml pooling destination tubes. **Setup pools in order from tube rack wells B1-D6 down the column then across the row.** For reagent setup, see 'Additional Notes' below.

---

You will need:
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [P50 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Eppendorf DNA/RNA LoBind Tube, 1.5 mL, VWR #80077-230](https://us.vwr.com/store/product/4675800/lobind-protein-or-genomic-microcentrifuge-tubes-eppendorf)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [Qiagen Buffer EB # 19086](https://www.qiagen.com/us/products/discovery-and-translational-research/lab-essentials/buffers-reagents/buffer-eb/#orderinginformation)
* Whole exome libraries

## Process
1. Upload your CSV file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol parses the input CSV file for wells and their respective volumes to transfer to each pool, as well as the buffer volume to transfer to each pool.
8. The first pool receives the specified sample volume from the specified wells for that pool. The correct pipette is automatically selected depending on transfer volume.
9. The first pool receives the specified volume of Buffer EB. The correct pipette is automatically selected depending on transfer volume.
10. Steps 8-9 are repeated for as many pools as input. The user is prompted to replace pools occupying tube rack wells B1-D6, as well as tipacks occupying slots 4 and 5 when necessary.

### Additional Notes
Reagent Setup:
* Qiagen Buffer EB: tube rack (slot 2) well A1
* Pool tubes (in order, loaded empty): tube rack (slot 2) wells B1-D6

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
vEx8HzVo  
1593

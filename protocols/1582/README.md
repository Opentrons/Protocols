# Custom Cartridge Filling

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol performs vape cartridge oil filling from a reservoir mounted on a temperature module to a custom 6x8 cartridge adapter. The protocol allows for the user to input the number of cartridges to fill, volume of oil with which to fill each cartridge, pipette mount side, and oil temperature to be heated to.

Please calibrate the pipette tip to the cartridge in the orientation shown in 'Additional Notes' below. It is very important that each cartridge is seated properly so that the dispenses land in the cartridge and not on the outside walls.

---

You will need:
* [Nalgene 300ml reservoir #1200-1300](https://www.thermofisher.com/order/catalog/product/1200-1300)
* [P1000 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [Opentrons 1000µl pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* Custom 5x6 cartridge adapter
* Vape cartridges

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Input the number of cartridges to fill, volume to fill, pipette mount, and oil temperature.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The temperature module reaches the input temperature before transfers begin.
8. The specified volume of oil is transferred to each cartridge in each adapter on the deck.
9. If necessary, the protocol pauses and prompts the user to reload oil and cartridges. The process repeats for as many cartridges as specified.

### Additional Notes

Proper Point of Calibration:
* ![Calibration Orientation](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1582/point_of_calibration.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
coVmAE82  
1582

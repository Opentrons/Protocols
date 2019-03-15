# Basic Liquid Transfer for Multiple Aliquots

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Distribution

## Description
This protocol performs a transfer of culture supernatant aliquots from 24-well deep well plates into 96-tube racks of matrix tubes. The protocol allows for user input of number of samples, number of aliquots per sample, and volume of each aliquot transfer. The quantity of each labware necessitated by the specified number of samples and aliquots is automatically calculated and prompts the user to load the proper quantities upon launching in the Run App.  

Each sample is iterated down each column and then across each row. If more than 24 samples are specified, the 25th sample is taken from the first well of the second deep well plate, and the transfers continue. Similarly, the destinations of the aliquots are oriented down each column and then across each row, before moving to the next destination tube rack. Aliquots of the same sample use the same tip and are filled vertically adjacent to each other on the 96-tube racks.

---

You will need:
* [ThermoFisher Matrix 1mL Tubes](https://www.thermofisher.com/order/catalog/product/3740TS)
* [Axygen 24-Deep-well Plate](https://www.fishersci.com/shop/products/axygen-storage-microplates-24-rectangular-deep-well-presterilized-clear-10ml/14222350)
* [P1000 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons 1000uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Download your protocol with desired number of samples, number of aliquots per sample, and volume of each aliquot transfer.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. For each sample, the specified volume of sample is distributed to as many tubes in the destination rack as aliquots per sample specified. This distribution uses the same tip for all aliquots of a sample, and then replaces the tip before the next sample's aspiration and distribution.
7. This process is for all samples across all deep well plates needed to hold the number of samples.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
3jhHe8dF  
1505

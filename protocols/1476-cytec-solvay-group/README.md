# Serial Dilution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Serial Dilution

## Description
With this protocol, your robot can perform serial dilutions up to 16 sample solutions. Robot will first transfer Solution A to all the destination tubes (C tubes). Robot will transfer serially dilute Solution B in tubes C.

---

You will need:
* P1000 Single-channel Pipette
* [Glass Dish](https://wheaton.com/dish-and-cover-20-slide.html)
* 30 mL vials
* Custom Tube Rack for 30 mL bottles
* 15 mL Conical Tubes
* [Opentrons 4-in-1 Tube Rack Sets](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 1000 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input the number of samples and dilutions you would like to output.
2. Set your solution A volume and dilution volume.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will transfer specified volume of solution A to 15 mL tubes.
9. Robot will transfer specified volume of solution B1 to C1, and serial dilute B1 accordingly to your input.
10. Robot will repeat step 9 for all of solution Bs.


### Additional Notes
Labware Setup:
* Solution A (Diluent): Glass Dish (slot 7)
* Solution B (Samples): 30 mL Serum bottles (slot 3, 6)
* Solution C (Outputs): 15 conical tubes (slot 1, 2, 4, 5)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
5XBtNepc
1476

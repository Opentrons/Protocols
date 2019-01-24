# PCR Prep: 3 Master Mixes

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
With this protocol, your robot can perform PCR with 24 samples, 3 control DNAs, and 6 gblocks.

---

You will need:
* P10 Single-channel Pipette
* P50 Single-channel Pipette
* [4-in-1 Tube Rack Sets](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 96-well Plate
* 10 uL Tiprack
* 50 uL Tiprack

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer 17 uL master mix 1 to row A-F of 96-well plate.
7. Robot will transfer 17 uL master mix 2 to H7-H12 of 96-well plate.
8. Robot will transfer 17 uL master mix 3 to H1-H6 of 96-well plate.
9. Robot transfer 3 uL each sample from microcentrifuge tubes to 3 wells of 96-well plate occupied with master mix 1 (see layout in Additional Notes below).
10. Robot will transfer 1 uL water to H7, and H8 of 96-well plate.
11. Robot will transfer 1 uL control DNA 1-3 to H10-H12 respectively.
12. Robot will transfer 1 uL gblock10 - gblock31250 to H1-H6 respectively.

### Additional Notes
![plate_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1478-kinnison-university-of-maine/plate_layout.png)

---

![tuberack_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1478-kinnison-university-of-maine/rack_layout.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
zl3Z69CO
1478

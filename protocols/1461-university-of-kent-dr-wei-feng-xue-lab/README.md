# Protein Quantification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
*
    *

## Description
Your robot can perform protein quantification using ThT and water following a specific layout, see Additional Notes.

---

You will need:
* P10 Single-channel Pipette
* P300 Single-channel Pipette
* 96-well Plate
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 10 uL Tip Racks
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select the container you are using to place the protein.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 99 uL protein to wells 2-6 and 10-11 in row B of the 96-well plate.
8. Robot will transfer 49 uL of protein to wells 2-6 and 10-11 in row C.
9. Robot will transfer 24 uL of protein to wells 2-6 and 10-11 in row D.
10. Robot will add buffer wells filled with protein in rows C and D to make 99 uL for wells in columns 2-6 and to make 100 uL for wells in columns 10-11.
11. Robot will add 1 uL of ThT to all wells filled with protein in column 2-6 and well B7.
12. Robot will add 99 uL of buffer to well B7.
13. Robot will fill all outermost wells and those adjacent to wells filled with protein or buffer with 100 uL of water.


### Additional Notes
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1461-university-of-kent-dr-wei-feng-xue-lab/layout.png)

---

15 mL Tube Rack Setup:
* Buffer: A1
* Water: B1
* (Protein: A2)

---

2 mL Eppendorf Tube Rack Setup:
* ThT: A1
* (Protein: A2)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
qyWDwQzn
1461

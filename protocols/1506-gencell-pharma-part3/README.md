# CGH Sure Print G3 Human test Part 3/4: Labeling Master Mix Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
Links:
* [Part 1: Digestion Mix Prep](./1506-gencell-pharma-part1)
* [Part 2: DNA Denaturation and Fragmentation](./1506-gencell-pharma-part2)
* [Part 3: Labeling Master Mix Preparation](./1506-gencell-pharma-part3)
* [Part 4: Hybridization Master Mix](./1506-gencell-pharma-part4)

This protocol allows your robot to create and distribute two different Labeling Master Mixes in 1.5 mL Eppendorf tube to samples and controls in 8-well PCR strips. Samples start at A1, down the column and then down the plate. Controls start at A6, down the column and then down the plate.

---

You will need:
* P10 Single-channel Pipette
* P50 Single-channel Pipette
* [4-in-1 Tube Rack Sets](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 8-well PCR Strips
* 10 uL Tip Racks
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Set the number of samples you will be processing.
2. Set the number of controls you will be processing.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will create the master mixes based on the number of samples and controls you have input, by transferring water, 5X RE buffer, 10X dNTPs, Cyc3 (master mix 1) or Cyc5 (master mix 2), and Exo Klenow to the master mix locations in the 2 mL tube rack.
9. Robot will transfer and mix 21 uL master mix 1 to samples (starting at A1).
10. Robot will transfer and mix 21 uL master mix 2 to controls (starting at A6).


### Additional Notes

4x6 Eppendorf Rack Setup: (slot 5)
* Water: A1
* 5X RE buffer: A2
* 10X dNTPs: A3
* Cyc3: A4
* Cyc5: A5
* Exo Klenow: A6
* Master Mix 1: D1
* Master Mix 2: D6

---


If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
epFuJxzU
1506

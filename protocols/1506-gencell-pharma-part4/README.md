# CGH Sure Print G3 Human test Part 4/4: Hybridization Master Mix

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

This protocol allows your robot to prepare and distribute the Hybridization Master Mix in a 1.5 mL Eppendorf tube to samples in 8-well PCR strips.

---

You will need:
* P300 Multi-channel Pipette
* P50 Multi-channel Pipette
* [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Temperature Module + Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* 8-well PCR Strips
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Set the number of samples you will be processing.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will create the master mixes based on the number of samples and controls you have input, by transferring Cot-1 DNA, 10X aCGH Blocking Agent, HI-RPM Hypridization Buffer to the master mix location in the 2 mL tube rack.
8. Robot will distribute the master mix to samples, starting at A1.


### Additional Notes
Temperature Deck Rack Setup: (slot 10)
* Cot-1 DNA: A1
* 10X aCGH Blocking Agent: A2

---

Room Temperature Rack Setup: (slot 4)
* Master Mix: A1
* HI-RPM Hypridization Buffer: A3

---

Tip Rack Setup:
* In order to use the multi-channel pipettes as single-channel pipettes, you will need to remove some tips from the tip racks for this protocol based on the following image:

![setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1506-gencell-pharma/tiprack-part4.png)

---


If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
epFuJxzU
1506

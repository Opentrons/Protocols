# mRNA Extraction Using Dynabeads

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to perform mRNA extraction for low input samples using [Dynabeads® Oligo (dT)25](https://www.thermofisher.com/us/en/home/references/protocols/nucleic-acid-purification-and-analysis/mrna-protocols/dynabeads-oligo-dt-25.html) with our Magnetic Module(https://shop.opentrons.com/products/tempdeck). The steps in the protocol include bead preparation, and direct mRNA isolation. A P50 single-channel and a P300 multi-channel pipette are required.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Module
* [MagDeck](https://shop.opentrons.com/products/tempdeck)

### Reagents
* [Dynabeads® Oligo (dT)25-61002](https://www.thermofisher.com/us/en/home/references/protocols/nucleic-acid-purification-and-analysis/mrna-protocols/dynabeads-oligo-dt-25.html)

## Process
1. Input the number of samples you are processing.
2. Input your desired wait time for beads to settle. (We recommend 5 minutes)
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".

Bead Preparation
8. Robot will resuspend the beads before transferring to the plate on the magnetic module.
9. Robot will remove supernatant.
10. Robot will wash the beads by resuspending in LBB+ buffer.

Direct mRNA isolation
11. Robot will remove supernatant.
12. Robot will transfer and mix sample lysate to washed beads.
13. Robot pause for user to place the plate on a plate mixer for at least 10 minutes for incubation. User will put the plate back on the magnetic module.
14. Robot will remove supernatant.
15. Robot will wash plate with Washing Buffer A.
16. Robot will wash plate with Washing Buffer B.
17. Robot will wash plate with LSB.
18. Robot will transfer Tris-HCl to the plate.
19. Robot will pause for user to place the plate on the temperature module. Plate will be incubated at 80°C for 5 minutes.
20. Robot will pause for user to place the plate back on the magnetic module.
21. Robot will transfer 30 uL supernatant to a fresh PCR plate.

### Additional Notes
* Deep well Plate setup
    * Dynabeads: **A1**

* Trough setup
    * LBB: **A1**
    * Washing Buffer A: **A2**
    * Washing Buffer B: **A3**
    * LSB: **A4**
    * Tris-HCl: **A5**
    * Liquid Trash: **A12**

* During setup, make sure to put an empty Biorad Hard-shell plate on the magnetic module. Your samples should be in a PCR plate in slot 2. A fresh PCR plate should be placed in slot 3.


###### Internal
V50NNMHp
1108

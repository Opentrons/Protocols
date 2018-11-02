# Zyppy™-96 Plasmid MagBead Miniprep: Part 2/2

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Sample Prep

## Description
Part 2 of 2: Purification of Plasmid DNA

Links: [Part 1](./1030-london-institute-of-medical-sciences-part1) [Part 2](./1030-london-institute-of-medical-sciences-part2)

This protocol allows your robot to perform the Zyppy™-96 Plasmid MagBead Miniprep. The Miniprep is the high-throughput, pellet-free method for *E. coli* plasmid DNA isolation.

This part requires the 96-well Block you have created using Part 1 of this protocol. Please see Additional Notes for more information on the setup.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* [MagDeck](https://shop.opentrons.com/products/magdeck)
* [TempDeck](https://shop.opentrons.com/products/tempdeck)

### Reagent
* [Zyppy™-96 Plasmid MagBead Miniprep](https://www.zymoresearch.com/zyppy)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer and mix 100 uL of Deep Blue Lysis Buffer to the 96-well block on the MagDeck in slot 1.
7. Robot will transfer 250 uL of Neutralization Buffer to the block on the MagDeck.
8. Robot will dispense 50 uL of MagClearing Beads to the block on the MagDeck.
9. Robot will engage the MagDeck for beads to separate from the lysate. 750 uL of the clear lysate will be transferred to a Collection Plate, 96-well block in slot 2.
10. Robot will prompt use to place the Collection Plate on the MagDeck and discard the original plate.
11. Robot will transfer 30 uL of MagBinding Beads to each well of the Collection Plate.
12. Robot will engage the MagDeck, and discard the clear lysates.
13. Robot will dispense 200 uL of Endo-Wash Buffer to each well of the Collection Plate.
14. Robot will engage the MagDeck, and discard the Endo-Wash Buffer.
15. Robot will prompt user to replenish all of the tipracks.
16. Robot will transfer 400 uL of Zyppy™ Wash Buffer to the Collection Plate.
17. Robot will eggage the MagDeck, and discard the Zyppy™ Wash Buffer.
18. Repeat steps 15-16.
19. Robot will set the temperature of the TempDeck to 65°C.
20. Robot will prompt user to place the Elution Plate in slot 2, and place the Collection Plate on the TempDeck for roughly 30 minutes/until the beads are no longer glossy.
21. Robot will dispense 40 uL of Zyppy™ Elution Buffer to each well of the Collection plate, and incubate on the TempDeck for 5 more minutes.
22. Robot will prompt user to place the Collection Plate back on the MagDeck.
23. Robot will engage the MagDeck, and transfer 30 uL eluates to the Elution Plate in slot 2.


### Additional Notes
Labware and Reagent Setup:
![setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1030-london-institute-of-medical-sciences/setup_part2.png)

Before you get started, read the [Instruction Manual](https://www.zymoresearch.com/media/amasty/amfile/attach/_D4100_D4101_D4102_Zyppy-96_MagBead_Miniprep_ver_1.1.0_AC.pdf) to make sure you have all the reagents and labware needed for this protocol.

If you have any questions regarding this protocol, please contact our protocol development team protocols@opentrons.com.


###### Internal
TGQnuJ7r
1030

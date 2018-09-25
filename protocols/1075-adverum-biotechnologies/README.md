# PCR/qPCR Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
With this protocol, your robot can perform qPCR prep with up to 20 samples on a 96-well plate. See Additional Notes for more information about the setup.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Input your number of samples.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 198 uL of PCR Dilution Buffer to a clean 96-well dilution plate.
8. Robot will transfer 2 uL of sample to the 96-well dilution plate.
9. Robot will aliquot 40 uL of DNase I solution to each well of a clean 96-well on the Temperature Module.
10. Robot will transfer the diluted samples from step 8 to each well of the microplate.
11. Robot will set the Temperature Module to 37° and incubate the plate for an hour.
12. Robot will add 50 uL of ProK mix to each well.
13. Robot will set the Temperature Module to 37° and incubate the plate for an hour.
14. Robot will increase the temperature of the module to 95° for 10 minutes.
15. Robot will drop the temperature of the module to 4°.
16. Robot will aliquot 245 uL of TE Buffer to the dilution plate, starting at well A4.
17. Robot will add 5 uL of sample to same well as step 16.
18. Robot will aliquot 7.5 uL of master mix to a new 96-well plate.
19. Robot will transfer 2.5 uL of standards in triplicate from A to G in columns 1-3.
20. Robot will transfer 2.5 uL the negative control in row H1-3.
21. Robot will transfer 2.5 uL of samples in triplicate from top down, left to right, starting in well A4.

### Additional Notes
* Trough Setup
    * Dilution Buffer: **A1**
    * TE Buffer: **A2**
* Tuberack setup
    * DNase I: **A1**
    * ProK Mix: **B1**
    * Master Mix: **C1**
* Your standards (A1-G1) and negative control (H1) should be in column 1 of the PCR strip in slot 5.

###### Internal
u0ZIciDH
1075

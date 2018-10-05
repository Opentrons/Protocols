# Cell Culture and PCR Lysis Assay: Part 2/3

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Trypsinization

## Description
Part 2 of 3: Custom Cell Culture

Links: [Part 1](./989-max-delbruck-center-part1) [Part 2](./989-max-delbruck-center-part2) [Part 3](./989-max-delbruck-center-part3)

With this protocol, your robot can perform cell feeding, trypsinization, pooling and PCR lysis on up to 96 cell samples. This protocol supports cell culture in a 24-well plate (max 24 samples/run) or 96-well plate (max 96 samples/run).

This is part 2 of the protocol: Trypsination and Pooling. The robot will initiate the cell dissociation process, which prepares the cells to be transferred to other vessels. The cells will be washed with three times. Half of the dissociated colony will be transferred to a new plate, and half will be pooled into a single Eppendorf tube.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Select your cell container type.
2. Select your multichannel pipette model and axis. Note that you can ONLY use single channel pipettes with 24-well plates, so these two fields will not be utilized in the protocol.
3. Select your single channel pipette model and axis.
4. Input your desired number of samples.
5. Input the volume of media in each well before the protocol begins.
6. Input the volume of trypsin to be transferred to each well.
7. Input your desired incubation time for trypsinization in minutes.
8. Input the wash volume and number of mixing to be used when washing the plate.
10. Input the new media volume you would like to add to each well after cell dissociation.
9. Download your protocol.
10. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
11. Set up your deck according to the deck map.
12. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
13. Hit "Run".
14. Robot will discard media from all wells in the old plate.
15. Robot will transfer trypsin to each well in the old plate and pause for incubation.
16. Robot will remove trypsin from all the wells.
17. Robot will wash each well by dispensing the wash solution in a circular motion in side the well and then discarding the solution. This process will be repeated twice.
18. Robot will add media to the disassociated cells.
19. Robot will transfer half of the content of each well to a new plate, and pool half of the volume to an eppendorf tube.

### Additional Notes
* Tube rack setup
    * Trypsin: **A1**
* 12-column Trough setup
    * Wash Solution: **A1-9**
    * Media: **A10**
    * Liquid Trash: **A12**

###### Internal
dog1ERZJ
989

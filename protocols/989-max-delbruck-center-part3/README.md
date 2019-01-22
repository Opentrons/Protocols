# Cell Culture and PCR Lysis Assay: Part 3/3

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Lysis

## Description
Part 3 of 3: Custom Cell Culture

Links: [Part 1](./989-max-delbruck-center-part1) [Part 2](./989-max-delbruck-center-part2) [Part 3](./989-max-delbruck-center-part3)

With this protocol, your robot can perform cell feeding, trypsinization, pooling and PCR lysis on up to 96 cell samples. This protocol supports cell culture in a 24-well plate (max 24 samples/run) or 96-well plate (max 96 samples/run).

This is part 3 of the protocol: PCR Lysis. The robot will remove old media from the plate and add a pre-made buffer for incubation.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Select your cell container type.
2. Select your pipette model and axis. Note that you can ONLY use single channel pipettes with 24-well plates, so these two fields will not be utilized in the protocol.
3. Select your reagent container type. Note that you can ONLY use the tube racks with a single channel pipette.
4. Input your desired number of samples.
5. Input the volume of media in each well before the protocol begins.
6. Input the volume of buffer to be transferred to each well.
7. Input your desired incubation time in minutes.
8. Download your protocol.
9. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
10. Set up your deck according to the deck map.
11. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
12. Hit "Run".
13. Robot will discard media from all wells in the old plate.
14. Robot will transfer pre-made buffer to each well of plate.
15. Robot will delay for incubation.

### Additional Notes
* Reagent container
    * Buffer: **A1**
* Trough
    * Liquid Trash: Starting at **A1**

###### Internal
dog1ERZJ
989

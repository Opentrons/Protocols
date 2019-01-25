# Cell Culture and PCR Lysis Assay: Part 1/3

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Cell Feeding

## Description
Part 1 of 3: Custom Cell Culture

Links: [Part 1](./989-max-delbruck-center-part1) [Part 2](./989-max-delbruck-center-part2) [Part 3](./989-max-delbruck-center-part3)

With this protocol, your robot can perform cell feeding, trypsinization, pooling and PCR lysis on up to 96 cell samples. This protocol supports cell culture in a 24-well plate (max 24 samples/run) or 96-well plate (max 96 samples/run).

This is part 1 of the protocol: Cell Feeding. The robot will transfer media from a container of choice to each well on the cell culture plate. The volume of the media is customizable as well.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Select your cell container type.
2. Select your pipette model and axis for cell feeding. Note that you can ONLY use single channel pipettes with 24-well plates.
3. Select your media container type. Note that you can ONLY use the tube racks with a single channel pipette.
4. Input your desired number of samples.
5. Input the volume of old media to discard.
6. Input the volume of fresh media to transfer to each well.
7. Select the tip use strategy for the entire run.
8. Download your protocol.
9. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
10. Set up your deck according to the deck map.
11. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
12. Hit "Run".
13. Robot will discard old media from each well of the plate to liquid trash.
14. Robot will transfer media from source container to each well of the plate, based on the number of samples you have entered.

### Additional Notes
Reagent Container:
* Fresh Media: **A1**
* Liquid Trash: starting at **A5**

* Select a pipette that can handle the entire media volume in the least number of transfers to minimize the protocol run time.

###### Internal
dog1ERZJ
989

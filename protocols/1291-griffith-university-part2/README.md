# Cell Culture Workflow for 337 samples: Part 2/3 - Sample Transfer

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Distribution

## Description
Part 2 of 3: Sample Transfer

Links:
* [Part 1: Cell and Media Distribution](./1291-griffith-university-part1)
* [Part 2: Sample Transfer](./1291-griffith-university-part2)
* [Part 3: Wash Plate](./1291-griffith-university-part3)

With this protocol, your robot will generate up to 4 destination plates by transferring samples from a master plate described in Additional Notes. A P300 single-channel and P300 multi-channel pipette are required for this protocol. You will also need [Biotix automation reservoirs](http://biotix.com/products/reservoirs/100-ml-automation-reservoir-sterilized/) and [Greiner Bio-One 384-well plates](https://www.usascientific.com/384-well-cellstar-black-clearbottom-tc-plate.aspx).

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input your desired sample volume.
2. Input your desired control volume.
3. Input the column of which the controls are placed in the control plates.
4. Input the number of plates you will be generating.
5. Download your protocol.
6. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".
10. Robot will transfer samples from master plate to destination plate.
11. Robot will transfer controls from control plates to destination plate.
12. Robot will prompt you to place a new destination plate.
13. Robot will repeat step 10-12 until all the destination plates have been filled.


### Additional Notes
![master_plate](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1291-griffith-university/part2/master_plate.png)

---

![control_plate](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1291-griffith-university/part2/control_plates.png)

---

![destination_plate](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1291-griffith-university/part2/destination_plate.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Zyf8IiT9
1291

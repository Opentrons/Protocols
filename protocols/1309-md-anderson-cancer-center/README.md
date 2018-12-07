# Flow Cytometry Protocol

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cytometry

## Description
With this protocol, your robot can transfer cell suspensions, antibodies, DAPI and PBS from various labware into a single 96-well plate. The contents of each occupied well will lastly be transferred into its corresponding [flow tube](https://www.southernlabware.com/culture-tube-12x75mm-5ml-polypropylene-pp-sterile-attached-dual-position-cap-25-bag-20-bags-cs-500-cs.html?utm_source=google_shopping&gclid=Cj0KCQiA8_PfBRC3ARIsAOzJ2upmnJQUOrYhyx7X455Nh90NjC9BSovHlN9sBDvs_UgJ01NtJZkXRfYaAr_xEALw_wcB). This protocol requires a Temperature Module, a P10 and a P300 single-channel pipette. You will need a custom tube rack for the flow tubes. Please contact info@opentrons.com regarding acquiring this tube rack.

The volume of antibodies to be transferred to each well will be defined in a CSV file. See Additional Notes for more details on the CSV format.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your CSV file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer 100 uL cell suspensions into the wells of the 96-well plate.
8. Robot will transfer and mix each antibody into their designed wells.
9. Robot will incubate the plate at 4°C for 20 minutes.
10. Robot will transfer 100 uL DAPI containing PBS to the occupied wells.
11. Robot will pause for user to centrifuge and remove contents from the plate.
12. Robot will transfer and mix 250 uL PBS into each occupied well and transfer the contents of the well into a flow tube.


### Additional Notes
CSV Format:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1309-md-anderson-cancer-center/csv_layout.png)
* Each cell represents the transfer volume in uL
* Each row represents one well in the 96-well plate; number of rows determines number of wells to fill
* Each column represents an antibody

---

Tube Rack Setup:
* Antibody 1: A1
* Antibody 2: B1
* Antibody 3: C1
* Antibody 4: D1
* Antibody 5: A2, etc.

---

Trough Setup:
* Cells: A1
* DAPI with PBS: A2
* PBS: A3

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
tjGTjIYk
1309

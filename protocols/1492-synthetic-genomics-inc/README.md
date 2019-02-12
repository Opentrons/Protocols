# Cell Normalization

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
With this protocol, your robot can perform cell normalization by pipetting variable volumes of buffer and culture from a 96-well plate to four 24-well output plates. Information of the transfers will be provided in the form of CSV. See Additional Notes for the required CSV layout.

---

You will need:
* P1000 Single-channel Pipette
* 96-well Plate
* 24-well Plates
* [1-well Reservoir](http://agilentmicroplates.com/products/201250-100/)
* 1000 uL Tip Racks


### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input your CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer buffer to the output plates.
8. Robot will mix and transfer the selected wells in the 96-well plate to the selected destination wells.


### Additional Notes
CSV Layout:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1492-synthetic-genomics-inc/csv_layout.png)

* Keep the headers
    * Make sure the order of the headers is the same as follows:
        * Source Well
        * Dest Plate: use 1-4 only (corresponding to plates in slot 3-6)
        * Dest well
        * Buffer Volume (in uL)
        * Culture Volume (in uL)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
fc8lhzVY
1492

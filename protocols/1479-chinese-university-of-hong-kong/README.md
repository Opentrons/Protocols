# DNA Concentration Normalization

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA Normalization

## Description
With this protocol, your robot can normalize concentration of DNA samples from 2 mL Eppendorf tubes in PCR strips. Volumes of DNA and buffer for each normalization will be provided by the user as a CSV file. See Additional Notes for more details.

---

You will need:
* P10 Single-channel Pipette
* P50 Single-channel Pipette
* PCR Strips
* [4-in-1 Tube Rack Sets](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your volume CSV.
2. Input the maximum reaction volume.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will distribute buffer to the destination wells described in the CSV.
9. Robot will transfer DNA samples to the destination wells based on the volumes described in the CSV.


### Additional Notes
Robot Setup:
* PCR Strips: slot 1
* 2 mL Eppendorf Tube Rack: slot 2 (Reagent)
* 2 mL Eppendorf Tube Racks: slot 3-6 (Samples)

---

CSV Layout:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/1479-chinese-university-of-hong-kong/csv_layout.png)

* keep the headers

---

Sample Sources and Destinations:

![transfer_info](https://s3.amazonaws.com/opentrons-protocol-library-website/1479-chinese-university-of-hong-kong/transfer_location.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ZVQte3dj
1479

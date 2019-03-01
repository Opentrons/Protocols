# DNA Assembly Part 1/2: Part-Linker Fusion

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA Assembly

## Description
Links:
* [Part 1: Part-Linker Fusion](./1510-ingenza-ltd-part1)
* [Part 2: DNA Assembly](./1510-ingenza-ltd-part2)

This protocol allows your robot to prepare for Part-Linker Fusion, at which it generates parts that will then be purified before the final assembly. During this protocol, three or more components are cherrypicked into a 96-well plate that is loaded with a master mix. The volume of each component and its source and destination will be provided in the form of a CSV file. See Additional Notes for the CSV requirement.

---

You will need:
* P10 Single-channel Pipette
* P50 Single-channel pipette
* 96-well PCR Plate(s)
* [Temperature Module + Aluminum Block Set](https://shop.opentrons.com/products/tempdeck)
* [24-Place Tube Rack + White Inserts](https://us.vwr.com/store/product/4907407/biomek-tube-rack-and-tube-inserts-beckman-coulter)
* 2 mL Screwcap Tubes
* 10 uL Tip Racks
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/products/tempdeck)

### Reagents

## Process
1. Upload your transfer volume CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Based each row of the CSV, the robot will transfer component into the specific destination.

### Additional Notes
Components:
* You can have up to 5 sets of components in 24-place tube racks
* MUST be in slot 1-5

---

Destinations:
* You can have up to 2 96-PCR plates as destinations
* MUST be in slot 9, and/or 6

---

CSV Layout:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1510-ingenza-ltd/part1_csv.png)

* Keep the headers
* If you would like the pipette to mix the destination after the transfer, use `Yes`, otherwise, leave the cell empty

--

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
6yw4dNPb
1510

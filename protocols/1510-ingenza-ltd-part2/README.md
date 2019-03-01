# DNA Assembly Part 2/2: DNA Assembly

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA Assembly

## Description
Links:
* [Part 1: Part-Linker Fusion](./1510-ingenza-ltd-part1)
* [Part 2: DNA Assembly](./1510-ingenza-ltd-part2)

This protocol allows your robot to prepare DNA assmebly, at which the purified parts are assembled into final vector. Each assembly is composed of a number of part sand one of two master mixes. The volume of each component and its source and destination will be provided in the form of a CSV file. See Additional Notes for the CSV requirement.

---

You will need:
* P10 Single-channel Pipette
* P50 Single-channel pipette
* 96-well PCR Plate(s)
* [24-Place Tube Rack + White Inserts](https://us.vwr.com/store/product/4907407/biomek-tube-rack-and-tube-inserts-beckman-coulter)
* 2 mL Screwcap Tubes
* 10 uL Tip Racks
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select your destination plate type.
2. Upload your transfer volume CSV.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Based each row of the CSV, the robot will transfer component into the specific destination.

### Additional Notes
Sources:
* Slot 5: 24-Place Tube Rack
* Slot 8: 96-PCR Tube
---

Destination:
* Slot 9
* Can be a flat 96-well PCR plate, 96-well Bio-rad Hardshell Plate, or a 384-well plate

---

CSV Layout:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1510-ingenza-ltd/part2_csv.png)

* Keep the headers
* If you would like the pipette to mix the destination after the transfer, use `Yes`, otherwise, leave the cell empty

--

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
6yw4dNPb
1510

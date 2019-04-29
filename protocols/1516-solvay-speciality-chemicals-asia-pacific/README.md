# Cherrypicking Consolidation in Custom Vials

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol allows your robot to consolidate up to 24 mother solutions in up to 72 custom vials. The mother solutions are stored in 50 mL conical tubes. The volume of each mother solution to be transferred to each vial will be provided in the form of a CSV file. See Additional Notes for more information on the CSV requirement. Based on how much each mother solution is needed, the robot will automatically calculate the number of tubes each mother solution stock would need for each run.

---

You will need:
* P300 Single-channel Pipette
* P1000 Single-channel Pipette
* [Opentrons Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* 8 mL Vials
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/products/tube-rack-set-1)
* Opentrons 300 uL Tip Racks
* 1000 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your volume CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer the specified volumes of mother solution 1 from the aluminum block to all of the vials defined in the CSV.
8. Robot will transfer the specified volumes of mother solution 2 from the aluminun block to all of the vials defined in the CSV.
9. Robot will repeat steps 7-8 until all of the mother solutions have been fully distributed to the custom vials.

### Additional Notes
CSV Layout:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1516-solvay-speciality-chemicals-asia-pacific/csv.png)

* Keep the headers
* Each row represents a single vial
* Each column represents the volume of each mother solution in uL to be transferred

---

Mother Solution setup:
* The maximum volume in the tube is 50 mL
* If the total volume of a mother solution (sum of the volumes in a single column) exceeds 50 mL, the robot will recognize 2 or more Eppendorf tubes will be used to store the mother solution
* Tube order (slot 2 -> slot 5 -> slot 8): A1, B1, A2, B2, A3, B3
---

Custom vial racks setup:
* Vial starts in A1 well (top left corner of the labware) in slot 1
* Vial order in each slot: A1, B1, C1..... D6

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
chiTALyJ
1516

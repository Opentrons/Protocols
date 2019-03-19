# 96-PCR Prep with Temperature Module

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
This protocol allows your robot to perform PCR prep on up to 96 DNA samples from 2 mL Eppendorf tubes. Master mix is first distributed to the output PCR plate from a 15 mL conical tube. DNA samples are then transferred to the PCR plate by row.

---

You will need:
* P10 Single-channel Pipette
* P300 Single-channel Pipette
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* 96-well PCR Plate
* [4-in-1 Tube Rack Sets](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 2 mL Eppendorf Tubes
* 15 mL Conical Tube
* 10 uL Tip Rack
* Opentrons 300 uL Tip Rack

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents

## Process
1. Set the number of samples to be processed.
2. Set the volume of master mix and DNA samples.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will set and wait for the Temperature Module to reach 4°C before proceeding.
9. Robot will distribute master mix to number of wells by row in the PCR plate based on the number of samples specified by the user.
10. Robot will transfer each sample from tube racks to each well by row in the PCR plate.


### Additional Notes
Sample Ordering:
1. Tube Rack slot 4
2. Tube Rack slot 5
3. Tube Rack slot 1
4. Tube Rack slot 2

---

PCR Well Ordering: A1, A2, A3...A12, B1, B2..H12

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Do8Mi2w1
1531

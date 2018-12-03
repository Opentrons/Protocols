# Clean Lab Protocol

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
This protocol is consisted of (1) Fragmentation, (2) End Repair, (3) Ligation Step 1, (4) MBC Adapter Incorporation, (5) Ligation Step 2, and (6) Cleanup. The number of samples processed in this protocol is *always* 8. Two Temperature Modules are required, please see Additional Notes for more information on using more than one Temperature modules on the robot.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/products/tempdeck)

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".


### Additional Notes
PCR Strip Tubes Setup: (slot 3)
* Samples: column 1
* 0.1M EDTA: column 2
* 2.5x AMPure beads: column 3
* AMPure beads: column 4
* 10mM TrisHCl: column 5
* Ligation beads: column 6
* Ligation Cleanup Buffer: column 7
* Ligation Cleanup Buffer: column 8
* Ultra-Pure water: column 9
* 0.5mM NaOH: column 10

---

Trough Setup: (slot 6)
* 70% Ethanol: well A1

---

Temperature Modules: 
* Slot 2: controlled outside of robot (4°C throughout entire protocol; see instructions below)
* Slot 11: controlled by the App (temperature changes automaticlaly)

---

Currently, multiple modules of the same type cannot be used in the robot at once. You can use on with the robot (coded in your protocol), and the rest of the them need to be controlled directly with a computer. Please see instructions [here](https://support.opentrons.com/ot-2/running-your-module-without-the-robot).

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
PuwggbMu
1431

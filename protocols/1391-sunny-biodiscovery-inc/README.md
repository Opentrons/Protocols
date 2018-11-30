# Cell Culture and Addition of Samples

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Cell Feeding

## Description
With this protocol, your robot can plate cells from a trough to a 96-well plate, as well as distribute several samples from 2-mL tubes to each well following a specific layout (see Additional Notes). This protocol requires a P10 single-channel and a P300 multi-channel pipette.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select the type of 2-mL tubes you will be using in this protocol.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will resuspend the cells in the trough and distribute to all wells on the 96-well plate except well A1 and A2.
8. Robot will use the same tip to mix before transferring tube 1, 2, 3, and 4 to the designated wells.
9. Robot will use the same tip to mix before transferring tube 5, 6, and 7 to the designated wells.
10. Robot will use the same tip to mix before transferring tube 8, 9, and 10 to the designated wells.
11. Robot will use the same tip to mix before transferring tube 11, 12, and 13 to the designated wells.
12. Robot will use the same tip to mix before transferring tube 14 and 15 to the designated wells.


### Additional Notes
Tube Rack Well Iteration:
* Tube 1: well A1
* Tube 2: well A2, etc

![setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/well_iteration_row.png)
---
96-Well Plate Layout:

![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1391-sunny-biodiscovery-inc/layout.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Nss467LB
1391

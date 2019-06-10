# NGS Library Prep-8 Samples

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
With this protocol, your robot can perform a part of the NGS library prep on 8 samples based on our [Omega Bio-tek Mag-Bind® TotalPure NGS protocol](./omega_biotek_magbind_totalpure_NGS).

See Additional Notes for protocol setup.

---

You will need:
* P50 Multi-channel Pipette
* 12-well Trough
* 96-well PCR Plate
* Bio-Rad Hardshell 96-well PCR Plate
* Magnetic Module
* TipOne 200 uL Tip Rack

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer and mix 16 uL AMPure XP Beads to 20 uL of PCR samples on the Magnetic Module.
7. After 2 minutes of incubation, magnetic module will be engaged and robot will remove supernatant.
8. Robot will wash the beads twice with 200 uL of 70% ethanol.
9. Robot will dry the beads for 5 minutes at room temperature.
10. Robot will resuspend the beads in 20 uL of H2O.
11. After 5 minutes of incubation, magnetic module will transfer supernatant to a clean output plate in slot 2.


### Additional Notes
Protocol Setup:

Make sure your reagents are setup as follows before the protocol begins.

![setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1495/setup.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
NUAi1xgJ
1495

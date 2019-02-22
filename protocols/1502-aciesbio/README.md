# Mag-Bind® Ultra-Pure Plasmid 96 Kit with Lysate Clearance via Magnetic Beads

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
With this protocol, your robot can perform extraction and purification of nucleic acids for up to 96 samples using the [Mag-Bind® Ultra-Pure Plasmid DNA Kit](http://omegabiotek.com/store/product/mag-bind-plasmid-endo-free-purification-kit/).

---

You will need:
* 96-well deep PCR plate
* 96-well flat PCR plate
* [12-row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* p300-Multi pipette
* p50-Multi pipette
* 200ul Tip rack
* 50ul Tip rack

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [MagDeck](https://shop.opentrons.com/products/magdeck)

### Reagents
* [Mag-Bind® Ultra-Pure Plasmid DNA 96 Kit](http://omegabiotek.com/store/product/mag-bind-plasmid-endo-free-purification-kit/)

## Process
1. Input your desire volume of elution buffer.
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer 250 uL Solution I/RNase A to each well of the plate in slot 2. Program will pause and prompt user to vortex the plate.
7. Robot will transfer 250 uL Solution II. Program will pause and prompt user to gently mix the plate and incubate the plate off-robot for 5 minutes.
8. Robot will transfer 125 uL N3 Buffer and 30 uL LC Beads to the plate.
9. Program will prompt user to mix the plate and place it on the *MagDeck*. A new plate will be placed by user in slot 2.
10. MagDeck will engage and supernatant will be transferred to the clean plate in slot 2. MagDeck will disengage.
11. Robot will transfer and mix 500 uL ETR Binding Buffer and 20 uL Mag-Beads® Particles RQ to the new plate. Plate is incubate in room temperature for 5 minutes.
12. Program will prompt user to discard the old plate on the *MagDeck* and replace it with the plate in slot 2.
13. MagDeck will engage and supernatant will be discarded in liquid trash container. MagDeck will disengage.
14. Robot will transfer 500 uL ETR Wash Buffer to the plate on the MagDeck.
15. MagDeck will engage and supernatant will be discarded in liquid trash container. MagDeck will disengage.
16. Program will prompt user to *replenish tipracks*.
16. Robot will add 700 uL VHB Buffer to the plate on the MagDeck.
17. MagDeck will engage and supernatant will be discarded in liquid trash container. MagDeck will disengage.
18. Repeat steps 16-17 for a second VHB Buffer wash.
19. Robot will add 700 uL SPM Wash Buffer to the plate on the MagDeck.
20. MagDeck will engage and supernatant will be discarded in liquid trash container.
21. Program will pause for 10 minutes to dry the Mag-Bind® Particles RQ. MagDeck will disengage.
22. Robot will add Elution Buffer to re-suspend the beads.
23. MagDeck will engage. Robot will transfer supernatant into a new 96-well plate in slot 5.

### Additional Notes
Before you begin the protocol, please read the [Product Manual](http://omegabiotek.com/store/wp-content/uploads/2014/01/M1258-Mag-Bind-Ultra-Pure-Plasmid-DNA-96-Kit-Combo-Online-010716.pdf) of the Mag-Bind® Ultra Pure Plasmid DNA Kit to make sure you have the correct labware and reagents. The protocol begins at step 4 in page 9 of the manual.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
BVjNKd5X
1502

# NGS Library Prep: NEB POLYdT Purification Kit

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biololgy
    * NGS Library Prep

## Description
With this protocol, your robot can perform NGS library prep using the [NEB POLYdT Purification Kit](https://www.neb.com/products/e7490-nebnext-polya-mrna-magnetic-isolation-module).

---

You will need:
* P10 Multi-channel Pipette
* P300 Multi-channel Pipette
* [Opentrons Magnetic Module](https://shop.opentrons.com/products/magdeck)
* [Biorad Hardshell Full-skirted 96-well PCR Plates](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* 96-Deep Well Plate

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)

### Reagents
* [NEB POLYdT Purification Kit](https://www.neb.com/products/e7490-nebnext-polya-mrna-magnetic-isolation-module)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer and mix Bead/Buffer Mix to each sample in plate A.
7. Robot will pause so that a step in the Thermocycler can be performed manually.
8. Robot will mix each well before incubating for 5 minutes in room temperature. Magnetic module will be turned on and pause for 1 minute.
9. Robot will remove supernatant from each well of plate A.
10. Robot will transfer Wash Buffer to each sample.
11. Robot will remove supernatant from each sample. Magnetic Module will be turned off.
12. Robot will add TAE and Binding Buffer to each sample.
13. Robot will pause for 5 minutes before turning on the Magnetic Module.
14. After 1 minute of incubation, robot will remove supernatant from each sample.
15. Robot will perform wash steps again by adding Wash Buffer and removing it thereafter.
16. Robot will add and mix Primer/Buffer Mix to each sample.
17. Robot will pause so that a Thermocycler step can be performed manually.
18. Robot will fill Plate C with RT mix.
19. Magnetic Module will be engaged. Robot will transfer RNA sample from plate A to plate C.


### Additional Notes
Variables:
* `bead_volume`: volume (uL) of Bead/Buffer Mix to be transferred to each sample
* `wash_buffer_volume`: volume (uL) of Wash Buffer to be transferred to each sample
* `TAE_volume`: volume (uL) of TAE to be transferred to each sample
* `binding_buffer_volume`: volume (uL) of Binding Buffer to be transferred to each sample
* `primer_mix_volume`: volume (uL) of Primer/Buffer Mix to be transferred to each sample
* `RT_mix_volume`: volume (uL) of RT Mix to be transferred to each sample
* `RNA_volume`: final volume (uL) of RNA sample to be transferred to new plate

---

Plate Setup:
* Plate A: slot 1
* Plate B: slot 2
* Plate C: slot 3
* Plate D: slot 4

---

Reagent Setup:
* Bead/Buffer Mix: Plate B column 1
* TAE: Plate B column 3
* Binding Buffer: Plate B column 5
* Primer/Buffer Mix: Plate B column 7
* RT Mix: Plate B column 9
* Wash Buffer: Plate D column 1-2

---

Throughout the protocol, the robot would pause and prompt you to refill the tip racks when they have run out. Please replenish the tip racks before resuming.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
n8FXZd8d
1436

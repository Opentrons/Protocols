# Nucleic Acid Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
This protocol performs nucleic acid purification on BioRad 96-well PCR plates. For reagent setup in a 12-row trough, see 'Additional Notes' below.

---

You will need:
* [P300 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [300ul TipOne Graduated Filter Tips #1120-9810](https://www.usascientific.com/300ul-tipone-filtertip.aspx)
* [BioRad 96-Well PCR Plates #MLP9601](http://www.bio-rad.com/en-us/sku/mlp9601-multiplate-96-well-pcr-plates-high-profile-unskirted-clear?ID=mlp9601)
* [12-Row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* Homebrew reagents

## Process
1. Input the volume of autoclave ddH2O, and upload your CSV file containing sample columns to process according to the example in 'Additional Notes' below. The columns should be entered as comma separated values on the same line
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 60ul of isopropanol is transferred from the trough to each of the specified sample columns on the starting sample plate. Samples are mixed 10x after each transfer, and new tips are used for each sample. Tips are returned.
8. Beads are mixed and 100ul of beads is distributed to each of the selected sample columns of a new plate on a disengaged magnetic deck using the same tips.
9. 160ul of samples are transferred from the original plate to their corresponding well of the plate on the magnetic deck (already containing beads). Samples are mixed 15x after each transfer, and new tips are used for each sample.
10. The plate incubates for 10 minutes, and the magnetic deck engages. Samples incubate on the magnet for 3 minutes for the beads to separate before the protocol resumes.
11. The aspiration flow rate is decreased to 25ul/s to avoid bead perturbation, and the supernatant is removed from each sample to the waste, using the corresponding tip from step 7. Tips are returned after the transfer.
12. The magnetic deck disengages, and the flow rate is increased back to 150ul/s. 150ul of wash buffer is distributed to the top of each sample well to avoid contamination. The tip used in the distribution is returned.
13. Each sample is mixed with its corresponding tip from step 7. Tips are returned.
14. The plate incubates for 2 minutes, and the magnetic deck engages. Samples incubate on the magnet for 3 minutes for the beads to separate before the protocol resumes.
15. The aspiration flow rate is decreased to 25ul/s to avoid bead perturbation, and the supernatant is removed from each sample to the waste, using the corresponding tip from step 7. Tips are returned after the transfer.
16. Steps 12-15 are repeated 1x more, and the magnetic deck disengages.
17. 30ul of DNase is transferred from the trough to each of the specified sample columns on the magnetic plate using a new tip. Samples are mixed 10x after each transfer, using the corresponding tip from step 7. Tips are returned. The samples incubate for 30 minutes.
18. 30ul of binding buffer is transferred from the trough to each of the specified sample columns on the magnetic plate using a new tip. Samples are mixed 10x after each transfer, using the corresponding tip from step 7. Tips are returned. The samples incubate for 5 minutes.
19. The magnetic deck engages, and samples incubate on the magnet for 3 minutes for the beads to separate before the protocol resumes.
20. The supernatant from each sample is transferred from the magnetic plate to the waste, using the corresponding tips from step 7.
21. Steps 12-15 are repeated 2x.
22. The plate incubates on the magnet for 3 minutes for the beads to dry, and the magnetic deck disengages.
23. The specified volume of autoclave ddH2O is transferred from the trough to each of the specified sample columns on the magnetic plate using a new tip. Samples are mixed 10x after each transfer, using the corresponding tip from step 7. Tips are returned. The samples incubate for 5 minutes.
24. The magnetic deck engages and the plate incubates on the magnet for 3 minutes for the beads to separate.
25. All but 2 ml of supernatant is removed from the samples to their corresponding wells on a new plate, using the corresponding tips from step 7. Tips are dropped after each transfer. The magnetic deck disengages.

### Additional Notes
![Example CSV](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1560-stenglein-lab-colorado-state-university/csv_example.png)

![Trough Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1560-stenglein-lab-colorado-state-university/trough_reagent_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
lyO3bXRq  
1560

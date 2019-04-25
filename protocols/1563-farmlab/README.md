# Nucleic Acid Purification

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
This protocol performs nucleic acid purification. The protocol allows the user to select the number of sample columns to be processed, incubation time on the magnetic block, number of mix repetitions, elution volume, and number of supernatant transfers. Tips are reused where possible to conserve tips while avoiding contamination.

---

You will need:
* [Bioke 4titude Open Reservoir](https://www.bioke.com/webshop/4ti/0131.html)
* [12-Row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Bio-Rad 96-Well PCR Plate](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [PlateOne 96-Well Deep Plate](https://www.usascientific.com/2ml-deep96-well-plateone-sterile.aspx)
* [VWR New Generation 200ul Tips #89079-458](https://us.vwr.com/store/product?keyword=89079-458)
* [P300 Multi-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)

### Robot
* [OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/labware/products/magdeck)

### Reagents
* [Mag-Bind Universal Pathogen 96 kit](https://www.omegabiotek.com/product/mag-bind-bacterial-dna-96-kit/)

## Process
1. Input values for the number of sample columns, minutes to incubate on magnetic block, number of initial mixes, number of secondary mixes, elution volume (ul), number of first supernatant transfers, and number of second supernatant transfers.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 180ul of each sample on the deep-well plate is mixed and transferred to the magnetic plate using different tips for each transfer. Tips are returned.
8. The magnetic deck engages, and the plate incubates for the specified number of minutes for the beads to separate out.
9. 200ul is transferred from each sample well to the waste reservoir using the corresponding tip from step 7 for each sample. Tips are returned, and the magnetic deck disengages.
10. Steps 7-9 are repeated for 4x more for a total of 5x.
11. New tips are used to transfer 180ul of VHB buffer to each sample on the magnetic plate and mixed the specified number of times, using different tips for each sample. Tips are returned.
12. The magnetic deck engages, and the plate incubates for the specified number of minutes for the beads to separate out.
13. 200ul is transferred from each sample well to the waste reservoir using the corresponding tip from step 11 for each sample. Tips are returned, and the magnetic deck disengages.
14. Steps 11-13 are repeated for as many times as specified.
15. New tips are used to transfer 180ul of SPM buffer to each sample on the magnetic plate and mixed the specified number of times, using different tips for each sample. Tips are returned.
16. The magnetic deck engages, and the plate incubates for the specified number of minutes for the beads to separate out.
17. 200ul is transferred from each sample well to the waste reservoir using the corresponding tip from step 15 for each sample. Tips are returned, and the magnetic deck disengages.
18. Steps 15-17 are repeated for as many times as specified.
19. Steps 15-17 are repeated 1x more, but the magnetic deck remains engaged.
20. New tips are used to transfer 180ul of water to each sample on the magnetic plate. 200ul is immediately transferred from each sample well to the waste reservoir using different tips for each sample.
21. The magnetic deck disengages.
22. The specified volume of elution buffer is transferred to each well of the magnetic plate and mixed the specified number of times using different tips for each transfer. Tips are returned.
23. The plate incubates for 5 minutes.
24. The magnetic deck engages and the plate incubates for another 5 minutes.
25. The specified volume of elution buffer is transferred to the corresponding wells on the new PCR plate using the corresponding tips from step 22. Tips are dropped after the transfer.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
LPEnFVpa  
1563

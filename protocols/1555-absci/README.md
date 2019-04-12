# Nucleic Acid Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
This protocol performs nucleic acid purification on custom 96 deep-well PCR plates. The protocol allows for the user to select the number of columns to be processed, as well as the type of pipette that will be used. To see diagrams for tube rack and trough reagent setup, see Additional Notes below.

---

You will need:
* [Simport Bioblock Deep-Well Plate](http://www.simport.com/products/deep-well-plates-and-cluster-tubes/deep-well-plates/t110-10-bioblock.html)
* [PlateOne Deep-Well Plate](https://www.usascientific.com/2ml-deep96-well-plateone-sterile.aspx)
* [Axygen 12-Row Trough](https://us.vwr.com/store/product/4694740/single-and-multi-well-reservoirs-axygen-scientific)
* [VWR Microcentrifuge Tube 1.7 mL](https://us.vwr.com/store/product/4674613/vwr-microcentrifuge-tubes-polypropylene)
* [Opentrons 300ul Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons P50 Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes)
* [Opentrons P300 Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* [Agencourt CosMCPrep Plasmid Purification Kit](https://www.beckman.com/reagents/genomic/dna-isolation/plasmid-purification)

## Process
1. Select the number of columns to process as well as the type of pipettes that will be used.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. RE1 is transferred to each sample on the bacteria plate and mixed after. New tips are used for each well.
8. L2 is transferred to each sample on the bacteria plate and mixed after. New tips are used for each well.
9. The plate incubates for 3 minutes at room temperature.
10. N3 is distributed to the top of each sample well on the bacteria plate to avoid contamination. The same tips are used for the entire distribution.
11. The protocol pauses and prompts the user to incubate the deep-well plate on orbital shaker for 10 minutes followed by centrifugation to pellet flocculent, and to replace the plate on the deck before resuming.
12. PUR4 is distributed to each well of the magnetic plate using a single tip (the protocol can accommodate this single tube transfer even with a multi-channel pipette.)
13. The first bacteria sample is transferred to its corresponding location on the magnetic plate. Tips are refreshed, and isopropanol is transferred to the destination well on the magnetic plate. The well contents are mixed, and the tips are dropped.
14. Step 13 is repeated for each bacteria sample.
15. The magnet is engaged, and the plate incubates on the magnet for 8 minutes.
16. Supernatant is removed from each well of the magnetic plate. New tips are used for each well.
17. EtOH is distributed to the top of each sample well on the magnetic plate to avoid contamination. The same tips are used for the entire distribution.
18. The plate incubates for 30 seconds after the last well receives EtOH.
19. EtOH is removed from each well of the magnetic plate. New tips are used for each well.
20. Steps 17-19 are repeated 2 additional times for a total of 3 washes.
21. The protocol delays for 10 minutes for the beads to dry on the magnetic plate.
22. RE1 is distributed to the top of each sample well on the magnetic plate to avoid contamination. The same tips are used for the entire distribution.
23. The magnet disengages, and the protocol prompts the user to incubate the elution plate at 37°C for 5 minutes followed by 30 seconds of vortexing to elute plasmid.

### Additional Notes
![Trough Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1555-absci/trough_setup.png)

![Tube Rack Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1555-absci/tuberack_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
TlnrfnpL  
1555

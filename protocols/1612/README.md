# Nucleic Acid Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
This protocol performs nucleic acid purification on a custom 96-deepwell plate mounted on an Opentrons magnetic module. For reagent setup and pooling scheme, see Additional Notes below.

---

You will need:
* [Greiner Sapphire PCR strips # 673273](https://shop.gbo.com/en/usa/products/bioscience/molecular-biology/thin-wall-pcr-tubes/pcr-8-tube-strips/673273.html)
* [Greiner Masterblock 2ml deepwell plate # 780270](https://shop.gbo.com/en/usa/products/bioscience/microplates/polypropylene-storage-plates/96-well-masterblock-2ml/780270.html)
* [USA Scientific 12-channel reservoir # 1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons P10 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons P300 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* Magnetic beads
* 80% EtOH
* 2-Propanol
* Elution buffer

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. PCR reactions from a PCR plate are pooled into a deepwell plate mounted on the magnetic module. For pooling scheme, see 'Additional Notes' below.
7. 5ul of magnetic beads are mixed and transferred to each of the new pools created on the magnetic plate, using new tips for each transfer.
8. 200ul of 2-propanol is transferred to each of the new pools.
9. Pools are agitated every 3 minutes for 15 minutes (5 total agitations)
10. The magnetic deck engages, and the protocol pauses for 2 minutes for the samples to incubate on the magnet.
11. Supernatant is transferred out to the liquid trash, using a new tip for each transfer.
12. The magnetic deck disengages, and 900ul of EtOH is transferred to each pool (directly onto the pelleted beads).
13. The contents of each well are mixed 5x to resuspend the beads in EtOH.
14. The magnetic deck engages, and the protocol pauses for 2 minutes for the samples to incubate on the magnet.
15. Supernatant is transferred out to the liquid trash, using a new tip for each transfer.
16. Steps 12-15 are repeated 1x more for a total of 2 ethanol washes.
17. Excess supernatant is transferred out using the P10 multi-channel pipette.
18. The protocol pauses for 10 minutes for the beads to dry, and step 17 is repeated.
19. The protocol pauses for 5 additional minutes for further drying.
20. The magnetic deck disengages, and 55ul of elution buffer is transferred to each pool (directly onto the pelleted beads).
21. The contents of each well are mixed 5x to resuspend the beads in elution buffer.

### Additional Notes
![Pooling Scheme](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1612/pool_scheme.png)

PCR strips setup:
* magnetic beads: strip 1 (all 8 tubes)

12-Channel trough setup:
* propanol: channel 1
* 80% EtOH: channel 2
* elution buffer: channel 3
* liquid trash: channel 12 (loaded empty)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
aqK02keb
1612

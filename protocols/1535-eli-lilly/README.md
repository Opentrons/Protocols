# NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library prep for a user-specified number of samples (maximum 24). Samples will begin in 2ml PCR strips on the temperature deck. Ensure samples are aligned down each column of the strips before moving across the row. See 'Additional Notes' below for tube and trough reagent setup.

---

You will need:
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* 200ul Pipette tips
* [2ml Tube racks](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 2ml Eppendorf tubes
* [12-Row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Bio-Rad Hard-Shell 96-Well PCR Plates #hsp9601](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* [CleanTag Small RNA Library Preparation Kit](https://www.trilinkbiotech.com/cart/coa/L3206_Insert.pdf)

## Process
1. Select the number of samples in the protocol.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Cleantag 3, RNase inhibitor, enzyme 1, and buffer 1 are transferred to each specified sample on the temperature deck. The contents of each sample well are mixed after the transfers.
8. The temperature deck sets to 28˚C, and the samples incubate for 1 hour.
9. The temperature deck heats to 65˚C, and the samples incubate for 20 minutes.
10. Water, buffer 2, RNase inhibitor, enzyme 2, and cleantag 5 are transferred to each specified sample well on the temperature deck.
11. The contents of each sample well are mixed after the transfers.
12. The temperature deck cools to 28˚C, and the samples incubate for 1 hour.
13. The temperature deck heats to 65˚C, and the samples incubate for 20 minutes.
14. RT primer is transferred to each specified sample on the temperature deck.
15. The temperature deck heats to 70˚C, and the samples incubate for 2 minutes.
16. Water, RT buffer, dNTP, DTT, RNase inhibitor, and RT enzyme are transferred to each specified sample well on the temperature deck.
17. The temperature deck cools to 50˚C, and the samples incubate for 1 hour.
18. PCR mastermix is distributed to each specified sample well on the temperature deck using the same tip.
19. Forward primer is transferred to each specified sample well on the temperature deck.
20. Barcoded index primers are transferred to their corresponding sample well on the temperature deck.
21. The protocol pauses and prompts the user to perform external thermocycling before resuming.
22. Once resumed, beads are distributed to each specified sample well on the temperature deck. The samples incubate for 10 minutes.
23. The protocol prompts the user to place the samples on the magnetic deck before resuming. The magnetic deck engages, and the samples incubate for 5 minutes.
24. Supernatant is removed from each sample and discarded using a new tip for each sample. The magnetic deck disengages.
25. Beads are distributed to each sample well on the magnetic deck. The magnetic deck engages, and the samples incubate for 5 minutes.
26. Supernatant is removed from each sample and discarded using a new tip for each sample. The magnetic deck disengages.
27. 2x 500ul ethanol washes are performed on all samples being prepared.
28. The beads airdry for 5 minutes, and the beads are resuspended in water.
29. The samples incubate on the magnet for 2 minutes, supernatant is transferred to a corresponding tube in a new clean tube rack.

### Additional Notes
![Tube Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1535/tube_setup2.png)

![Trough Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1535/trough_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
2OpU8JP9
1535

# NGS Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library prep for a specified number of sample columns using 2 magnetic modules. For instructions on setting up 2 magnetic modules for simultaneous use on your OT-2, please see 'Additional Notes' below.

---

You will need:
* [Bio-Rad Hard-Shell 96-Well PCR Plates, High Profile, Semi Skirted #HSS9601](http://www.bio-rad.com/en-us/sku/hss9601-hard-shell-96-well-pcr-plates-high-profile-semi-skirted-clear-clear?ID=HSS9601)
* [Hard-Shell 96-Well PCR Plates, Low Profile, Thin Wall, Skirted #HSP9641](http://www.bio-rad.com/en-us/sku/hsp9641-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-green-clear?ID=HSP9641)
* [12-Row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [P10 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P300 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [TipOne 10µl Filter Tips #1180-3710](https://www.usascientific.com/10ul-tipone-rpt-elongated-filter-tip-cassette.aspx)
* [TipOne 200µl Filter Tips #1180-8710](https://www.usascientific.com/200ul-tipone-rpt-filter-tip-cassette.aspx)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Modules](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* [Ampure XP Beads](https://www.beckman.com/reagents/genomic/cleanup-and-size-selection/pcr)
* [10x Diluted TE Buffer](https://www.thermofisher.com/order/catalog/product/12090015)
* 80% Ethanol

## Process
1. Input the number of sample columns, and set up your 2 magnetic modules (according to the instructions listed in 'Additional Notes' below).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The Ampure Beads are mixed and transferred to all specified wells in plate 1 (mounted on magnetic module 1). The contents of the plate are mixed after, and new tips are used for each transfer.
8. While plate 1 incubates, beads are distributed to the specified wells of plate 2 (mounted on magnetic module 2). The contents of The contents of the plate are mixed after, and new tips are used for each transfer.
9. Magdeck 1 engages and plate 1 incubates for 5 minutes.
10. The supernatant from each well of plate 1 is transferred to the corresponding well of plate 2. The contents of plate 2 are mixed after. New tips are used for each transfer and mix. Plate 2 incubates for 3 minutes after the last transfer.
11. Magdeck 2 engages and plate 2 incubates for 5 minutes.
12. Supernatant from each well of plate 2 is discarded in the liquid trash. New tips are used for each transfer.
13. Ethanol is slowly distributed to all sample wells of plate 2, and the plate incubates for 20 seconds.
14. The ethanol is slowly aspirated out of each well to the liquid trash. New tips are used for each transfer and returned for later use.
15. Steps 13-14 are repeated 2x more for a total of 3 ethanol washes. The same tips are used and discarded after the final ethanol wash.
16. The P10 multi-channel pipette discards any remaining ethanol from the wells. New tips are used for each of these transfers.
17. Magdeck 2 disengages.
18. TE buffer is transferred to all specified wells in plate 2. The contents of the plate are mixed after, and new tips are used for each transfer.
19. Magdeck 2 engages and plate 2 incubates for 1 minute.
20. The TE is transferred from each well to its corresponding well in plate 3. New tips are used for each transfer and returned for later use.
21. Steps 17-20 are repeated 1x more for a total of 2 TE transfers. After the second transfer, the wells of plate 3 are mixed and the tips are discarded.

### Additional Notes
In order to control two Magnetic Modules in the protocol, please follow the instructions below. You will need to modify the code in line 26 and 27.
1. Plug in Magnetic Module 1 to the robot.
2. SSH into the robot to gain access of it's terminal by running `ssh root@ROBOT_IP` (replace ROBOT_IP with your robot's IP)
3. Find device path of the module by running `ls /dev/ttyACM*`
4. Replace line 26 example device path with your result.
5. Unplug Magnetic Module 1, and plug in Magnetic Module 2.
6. Repeat the same steps above to find the device path and replace it in line 27.
7. Plug Module 1 back in.

---

![Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1579/reagent_setup.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
mgeGgwP3  
1579

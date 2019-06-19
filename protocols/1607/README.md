# Cell Culture Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs a cell culture assay on 4 custom 24-well culture plates. Ensure the plates are each mounted on temperature modules with aluminum plates mounted. For information on setting up 4 temperature mdoules for use at the same time, as well as reagent setup, see Additional Notes below.

---

You will need:
* [Cellvis 24-well glass-bottom plates # P24-1.5H-N](https://www.cellvis.com/_24-well-glass-bottom-plate-with-high-performance-number-1.5-cover-glass_/product_detail.php?product_id=49#dimension-diagram)
* [Opentrons 15-50ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 50ml Falcon tubes
* [Opentrons P1000 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 1000ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons Temperature Modules with aluminum block sets](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents
* Tissue culture media

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. The 4 temperature decks set to 37˚C. The protocol does not continue until the temperature is reached.
7. For each well in each plate, the old media is transferred out and blown out into a custom trash container (slot 1). A new tip then transfers fresh media from one of the media tubes using accurate height tracking.

### Additional Notes
In order to control two Temperature Modules in the protocol, please follow the instructions below. You will need to modify the code in line 21 and 22.

1. Plug in Temperature Module 1 to the robot
2. SSH into the robot to gain access of it's terminal by running ssh root@ROBOT_IP (replace ROBOT_IP with your robot's IP)
3. Find device path of the module by running ls /dev/ttyACM*
4. Replace line 24 example device path with your result
5. Unplug Temperature Module 1, and plug in the next temperature module.
6. Repeat steps 1-5 to find the device paths of the remaining 3 temperature modules and replace in lines 25-27.

---

15-50ml Tuberack setup:  
* fresh media: 50ml tubes in wells A3 & A4 **(each filled to at least 2cm below the top lip of the tube to ensure accurate height tracking)**

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
B4TutpJi  
1607

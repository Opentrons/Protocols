# NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library preparation for up to 96 samples. For notes on setting up 2 temperature modules for simultaneous use, as well as reagent setup for the protocol, please see 'Additional Notes' below.

---

You will need:
* [Abgene 96-Deepwell 0.8mL Polypropylene Storage Plate # AB-0765](https://www.thermofisher.com/order/catalog/product/AB0765?SID=srch-hj-AB-0765)
* [Opentrons 2ml Tube Rack with screwcap tubes](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [USA Scientific 12-channel reservoir # 1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons P10 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons P50 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [10ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons Temperature Modules](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) with [96-well aluminum blocks](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* [Lexogen QuantSeq 3' FWD kit](https://www.lexogen.com/quantseq-3mrna-sequencing/)

## Process
1. Input the number of samples to be processed, pipette mount sides, and whether dual indexes will be used.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
In order to control two Magnetic Modules in the protocol, please follow the instructions below. You will need to modify the code in line 27 and 28.

1. Plug in Temperature Module 1 to the robot.
2. Open the Terminal application on your computer.
3. SSH into the robot to gain access of it's terminal by running `ssh root@ROBOT_IP` (replace 'ROBOT_IP' with your robot's IP)
4. Find device path of the module by running ls /dev/ttyACM*
5. Replace line 27 example device path with your result (the `*` character will be replaced with a number).
6. Unplug Temperature Module 1, and plug in Temperature Module 2.
7. Repeat the same steps above to find the device path and replace it in line 28.
8. Plug Module 1 back in.

---

2ml Screwcap tube setup in Opentrons 4x6 tuberack:  
* FS1: well A1
* RS: well B1
* SS1: well C1
* MM2: well D1
* MM3: well A2

PCR strip setup (mounted on temperature module 2 with aluminum block):  
* MM1: strip 1 (wells A1:H1)

12-Channel reagent trough setup:
* PB: channel 1
* EB: channel 2
* PS: channel 3
* EtOH: channels 4-7
* liquid waste: channels 8-12 (loaded empty)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
eNlwMEdl  
1585

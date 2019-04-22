# High Throughput leChRO-seq Day 2: 2nd Bead Wash and Enrichment

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* NGS Library Prep
    * High Throughput leChRO-seq

## Description
Links:
* [Day 1-A: Run-on Reaction and Cleanup of Biotin-11 Run-on Reaction Part 1](./1534-cornell-university-part1)
* [Day 1-B: Run-on Reaction and Cleanup of Biotin-11 Run-on Reaction Part 2](./1534-cornell-university-part2)
* [Day 1-C: Decapping, 5’ Phosphorylation, and 1st Bead Binding and Enrichment](./1534-cornell-university-part3)
* [Day 2: 2nd Bead Wash and Enrichment](./1534-cornell-university-part4)
* [Day 3-A: 2nd Bead Binding and Enrichment](./1534-cornell-university-part5)
* [Day 3-B: Reverse Transcription](./1534-cornell-university-part6)

This protocol follows Day 2 of the High Throughput leChRO-seq protocol (steps 73-114).

Before you run the protocol, make sure you read the leChRO-seq Robot Protocol thoroughly. Master mixes used in this protocol will be prepared manually. Refer to Additional Notes at the bottom of this page for setup information.

After this part of the protocol is done, you need to perform the steps describe in the protocol manually (steps 115-139) before incubating the samples in the thermal cycler overnight, which marks the end of day 2.

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".


### Additional Notes
In order to control two Temperature Modules in the protocol, please follow the instructions below. You will need to modify the code in line 21 and 22.
1. Plug in Temperature Module 1 to the robot
1. SSH into the robot to gain access of it's terminal by running `ssh root@ROBOT_IP` (replace ROBOT_IP with your robot's IP)
2. Find device path of the module by running `ls /dev/ttyACM*`
3. Replace line 21 example device path with your result
4. Unplug Temperature Module 1, and plug in Temperature Module 2
5. Repeat the same steps above to find the device path and replace it in line 22

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
hdgDcxJ2
1534

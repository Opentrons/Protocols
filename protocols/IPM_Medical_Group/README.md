# Mass Spec Sample Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol allows the robot to transfer solutions between containers in custom racks, standard trough, and our 4-in-1 tube rack. The number of wells to fill in the MCT racks depends on the number of samples in each run, the number must be within 10-48.

Steps:
1. Pre-wet new tip. Transfer 30 uL of buffer from well A1 of trough to each well in the MCT tube racks, using the same tip.
2. Pre-wet new tip. Transfer 20 uL of enzyme from well A2 of trough each well in the MCT tube racks, using the same tip.
3. Pre-wet new tip. Transfer 50 uL of Internal Standard from well A3 of reagent trough to each well in the MCT tube racks, using the same tip.
4. Pre-wet new tip for each transfer: transfer 100 uL of sample from custom tube rack to corresponding well in the MCT racks.
5. Pause for incubation.
6. Pre-wet new tip. Transfer 350 uL of diluent from well A4 of reagent trough to each well in the MCT racks.
7. Pause for centrifuge.
8. New tip for each transfer: transfer supernatent from MCT well to corresponding well in vial rack.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".

### Additional Information
* Make sure to adjust the sample number at the top of the code to fit your experiment.
* Incubation time and centrifuge time are adjustable. If wait time is unpredictable, line 71 and line 77 can be changed to robot.pause(), which would cause the protocol to pause while running the protocol. User will have the ability to resume the run on the OT App after each incubation and centrifugation.

###### Internal
aAJeSyVX
1078

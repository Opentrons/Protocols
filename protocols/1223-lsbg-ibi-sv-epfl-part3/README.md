# RNA Mixing at Room Temperature: 96 Samples

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Mapping

## Description
This protocol allows your robot to mix 96 RNA samples with primers and water in a plate that is stayed at room-temperature. The volumes of RNA and water in each well vary and therefore, with be defined by two separate CSVs (see Additional Notes). Both the RNA plate and the primer plate are maintained at 4°C on a TempDeck. Please see Additional Notes for more information on using two TempDecks on the robot.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* [TempDeck](https://shop.opentrons.com/products/tempdeck)

## Process
1. Input the volume of primer to be transferred to each well.
2. Upload your water volume CSV.
3. Upload your RNA volume CSV.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will transfer each primer to each well on the plate.
10. Robot will distribute water to each well on the plate.
11. Robot will transfer RNA sample to each well on the plate.

### Additional Notes
Setup
* 2 mL Tube Rack: Slot 1
* RNA Plate on TempDeck: Slot 4
* Primer Plate on TempDeck: Slot 7 (TempDeck controlled outside of robot)
* Receptor Plate: Slot 8  

![csv setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1223-lsbg-ibi-sv-epfl/volume_csv_3.png)  
Volume CSV Template:
* 12 x 8 (columns x rows)
* Each cell represents the volume to be transferred in each well
* No headers are needed


Currently, multiples modules of the same type cannot be used in the robot at once. You can use one with the robot (in your protocol), the rest of them will need to be controlled with a computer. Please see the instructions [here](https://support.opentrons.com/ot-2/running-your-module-without-the-robot).

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
qNSHMgnB
1223

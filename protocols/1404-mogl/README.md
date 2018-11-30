# Dilution And 1st qPCR

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
This protocol allows your robot to serially dilute 8 samples in a PCR strip, and use perform PCR on two dilutions in triplicate from each sample. Your PCR strip tubes and output plate will be placed on the TempDecks. Please see Additional Notes for more information on using two TempDecks on the robot.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [TempDeck](https://shop.opentrons.com/products/tempdeck)

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".


### Additional Notes
![setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1404-mogl/setup.png)  
* Samples are pre-loaded in column 1 of the PCR Strip Tubes on the TempDeck.
* Standards are in column 12.
---
Reagent Setup
* Water: trough well A1
* Master Mix: tube rack well A1
---
Temperature Modules
* Slot 2: controlled outside of robot [4°C throughout entire protocol; see instructions below]
* Slot 4: controlled by the App [temperature changes automatically]

Currently, multiples modules of the same type cannot be used in the robot at once. You can use one with the robot (in your protocol), the rest of them will need to be controlled with a computer. Please see the instructions [here](https://support.opentrons.com/ot-2/running-your-module-without-the-robot).

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
LRjF66kI
1404

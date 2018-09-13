# Bead Cleanup

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Filling

## Description
This protocol allows the robot to distribute magnetic beads from a 1.5 mL tube to a number of wells in PCR strips, based on the number defined by the user. The beads are then washed with the use of the Opentrons MagDeck. This protocol can work with up to 32 samples.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### modules
* [MagDeck](https://shop.opentrons.com/products/magdeck)

## Process
1. Change the number of samples in the custom field above.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run.
7. Transfer 20 uL magnetic beads to PCR strips 1. Engage MagDeck for 3 minutes.
8. Remove 20 uL from PCR strips 1 to liquid trash. Disengage MagDeck.
9. Transfer and mix 23 uL from PCR strips 2 to PCR strips 1.
10. Incubate for 10 minutes.
11. Engagae MagDeck for 3 minutes. Remove 21 uL from PCR strips 2 to PCR strips 3.

### Additional Notes
* Set up your PCR strips in this way:
    * strips 1 in columns 1, 4, 7, 10
    * strips 2 in columns 2, 5, 8, 11
    * strips 3 in columns 3, 6, 9, 12

    ![PCR strips setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/bead_cleanup_pcr_strip.png)

###### Internal
hVZ487Gn
803

# Protein Crystallization Screen

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Distribution

## Description
This protocol performs liquid transfer from a 96 deep well block to the square resorvoirs of crystallography plates. The user can input any number of deck refills as well as transfer volume to each well. Each full deck transfer fills 9 plates from the deep well block by column using a P300 multi-channel pipette. If the user specifies more than 1 deck transfer, the robot pauses after each transfer and prompts the user to remove the filled plates and empty tip rack and replace empty plates and fresh tips on the deck.

---

You will need:
* [96 Starlab Deep Well Block](https://www.starlabgroup.com/en/consumables/plates_WebPSub-155857/deepwell-plates_PF-SL-155338.html)
* [Swissci SD3 3 Well Crystallization Plate](https://hamptonresearch.com/product_detail.aspx?cid=10&sid=182&pid=568)
* [P50 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [P300 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons 300uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [BCS Screen](https://www.moleculardimensions.com/products/c497-The-BCS-Screen/)
* [JCSG-plus](https://www.moleculardimensions.com/products/c343-JCSG-iplusi/)
* [Morpheus](https://www.moleculardimensions.com/products/c344-Morpheus/)
* [LMB Crystallization Screen](https://www.moleculardimensions.com/products/c489-The-LMB-Crystallization-Screen/)
* [PACT premier](https://www.moleculardimensions.com/products/c342-PACT-ipremieri/)
* [SG1 Screen](https://www.moleculardimensions.com/products/c410-SG1-Screen/)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. The multi-channel pipette picks up clean tips. The user specified transfer volume is transferred from column 1 of the deep well block to the square resorvoirs of column 1 of each of 9 plates occupying the deck. The tips are then dropped.
7. Step 6 is repeated for columns 2-12 of the block and plates.
8. If the user specifies more than 1 deck transfer, the robot pauses and prompts the replacement of the now filled plates with fresh plates, as well as the replacement of the empty tip rack with a full tip rack.
9. Steps 6 and 7 are repeated for as many deck transfers as specified.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Dc0h3WUW  
1526

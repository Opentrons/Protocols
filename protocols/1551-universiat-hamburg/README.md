# Biofilm Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Biofilm

## Description
This protocol performs a biofilm assay in a 24-well plate with the use of the Opentrons temperature module. Water, crystal violet, and acetic acid are each stored in one row of a 12-row trough (see Additional Notes below for proper reagent setup).Each reagent is consolidated into a 50ml tube.

---

You will need:
* [Opentrons P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/hardware-modules/products/single-channel-electronic-pipette?variant=5984549109789)
* [Opentrons 300ul Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [50ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [12-Row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* 50ml Tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents
* Water
* Crystal violet
* Acetic acid

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. The temperature module heats to 60˚C before the protocol begins.
7. The protocol prompts the user to place the 24-well plate on the temperature module and allow to incubate for 60 minutes.
8. Once the protocol is resumed, the temperature module will cool to 22˚C before the protocol resumes.
9. 250ul of crystal violet is distributed from the 12-row trough to each well in the 24-well plate using the same tip.
10. The protocol pauses for the plate to incubate for 5 minutes.
11. The crystal violet is consolidated from each well of the plate to one 50ml tube. A new tip is used for each well transfer, and the liquid is aspirated from 1ml above the bottom of the well.
12. 750ul of water is distributed from the 12-row trough to each well of the plate using the same tip.
13. Each well of the plate is mixed 10x with 300ul and consolidated to a new 50ml tube via transfer 1ml about the bottom of the sample well.
14. Steps 12-13 are repeated 2 additional times.
15. The protocol pauses for the temperature module to heat to 37˚C. Once the temperature is reached, the plate incubates for 30 minutes.
16. 750ul of water is distributed from the 12-row trough to each well of the plate using the same tip.

### Additional Notes
![Trough Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1551-universiat-hamburg/trough_reagent_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
4F4QLuWb  
1551

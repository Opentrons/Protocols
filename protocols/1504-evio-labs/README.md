# Evio Labs PCR/qPCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR

## Description
With this protocol, your robot can perform PCR/qPCR preparation on 24 samples with 2 sets of master mix (1 for bacteria and 1 for fungi) on a single 96-well plate. Bacteria samples occupy wells B2:G5, and fungi samples occupy wells B8:G11 to avoid edge effects.

---

You will need:
* P10 Single-channel Pipette
* P300 Single-channel Pipette
* 96-well PCR Plates
* [Aluminum Blocks](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [24-well 2ml Eppendorf Tube Racks](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 10 uL Tip Racks
* Opentrons 300 uL Tip Rack


### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer the first bacteria and fungi mastermixes to their respective corresponding output wells on PCR plate 1.
7. Robot will transfer samples from 2ml tubes to their corresponding wells on PCR plate 1.
8. Robot will pause for the user to spin down and thermocycle PCR plate 1, as well as load PCR plate 2.
9. Robot will transfer the second bacteria and fungi mastermixes to their respective corresponding wells on PCR plate 2.
10. Robot will transfer contents from PCR plate 1 to their respective corresponding wells on PCR plate 2.


### Additional Notes

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
fc8lhzVY
1492

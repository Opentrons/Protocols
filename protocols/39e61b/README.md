# Sample Transfer

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Well-to-well Transfer

## Description
This protocol performs DNA sample transfer from a PCR plate to E. coli samples in a PCR plate mounted on an Opentrons temperature module. All transfers are one-to-one. E. coli samples are mixed at a decreased flow rate after each transfer, and new tips are used for each transfer and mix sequence.

---

You will need:
* [Bio-Rad Hard-Shell 96-Well PCR Plates # hsp9601](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Opentrons P10 electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes)
* [Opentrons 10ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons temperature module with aluminum block for 96-well plate](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Upload your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. DNA samples are transferred to their corresponding wells on the E. coli plate (mounted on the temperature module). E. coli samples are mixed at a decreased flow rate after each transfer, and new tips are used for each transfer and mix sequence.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
39e61b

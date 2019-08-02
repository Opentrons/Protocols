# PCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs PCR preparation on a 96-well PCR plate mounted on an aluminum block on an Opentrons temperature module (set to 4˚C). Oligo primers are located in a separate 96-well PCR plate, and master mix is held in two screwcap tubes in an Opentrons aluminum block for 2ml screwcap tubes.

---

You will need:

* [Bio-Rad Hard-Shell 96-Well PCR Plate, low profile # HSP9601](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Bio-Rad Hard-Shell 96-Well PCR Plate, high profile # HSP9641](http://www.bio-rad.com/en-us/sku/hss9641-hard-shell-96-well-pcr-plates-high-profile-semi-skirted-green-clear?ID=hss9641)
* [Opentrons P50 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P50 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons 300ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons aluminum block set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons temperature module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Upload your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 20ul of mastermix (from 2 screwcap tubes) is distributed to each well of the PCR plate on the temperature module. After half the PCR wells receive mastermix, the remaining mastermix from tube 1 is transferred to tube 2; subsequent distributions are taken from tube 2. All dispenses move to the top of the PCR wells, so the same tip is used for the entire distribution.
8. 5ul of each oligo primer is transferred to its corresponding well on the PCR plate. New tips are used for each transfer to avoid cross contamination.

### Additional Notes
Reagent setup in 4x6 aluminum block for 2ml screwcap tubes:  
* mastermix: tubes A1 and A2

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
4c464f

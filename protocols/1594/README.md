# PCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs PCR preparation for a user-input number of 96-well sample plates (up to 5 per protocol). **Be sure to specify how high the mineral oil is filled to (in mm below the top opening of the trough). This will ensure accurate height tracking when aspirating mineral oil and will minimize excess oil left on the tip.** For reagent setup, see 'Additional Notes' below.

---

You will need:
* [P10 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [P50 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [Starlab 10ul and 50ul and Pipette tips](https://www.starlabgroup.com/en/consumables/pipette-tips_WebPSub-155853/tipone-filter-tips_PF-SL-154834.html)
* [Starlab 12-channel reservoir](https://www.starlabgroup.com/GB-en/consumables/reagent-reservoirs_WebPSub-155861/12-channel-reservoir_SLE2310-1200.html)
* [Starlab 96-well PCR plate](https://www.starlabgroup.com/en/consumables/pcr-consumables_WebPSub-155858/96-well-pcr-plate-skirted-low-profile_SLE1403-5200.html)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [Bioline MyFi mix # 25049](https://www.bioline.com/us/myfi-mix.html)
* [Fisher Mineral oil # 415080010](https://www.fishersci.com/shop/products/mineral-oil-pure-acros-organics-4/AC415080060)

## Process
1. Select the number of destination plates, volume of mineral oil (in ul) to transfer to each well, and distance form the oil surface to the opening of the trough (in mm).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The user input volume of mineral oil is transferred to each well of each destination plate on the robot deck. The aspirate and dispense flow rates are decreased 5x to accommodate viscous liquid. The protocol calculates the height from which to aspirate to ensure accurate pipetting of viscous liquid. Tips are reused for each dispense
8. 18ul of PCR mastermix is transferred to each well of each destination plate on the robot deck. The aspirate and dispense flow rates are restored to default.
9. 1ul of forward primer is transferred to each well of each destination plate on the robot deck. Tips are changed between each transfer to prevent sample contamination.
10. 1ul of reverse primer is transferred to each well of each destination plate on the robot deck. Tips are changed between each transfer to prevent sample contamination.

### Additional Notes
Reagent trough setup (slot 1):
* mineral oil: channel 1
* PCR mastermix: channel 3

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
pfoC2CnI  
1594

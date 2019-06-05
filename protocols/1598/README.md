# Biological Aliquots Transfer

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Distribution

## Description
This protocol performs biological aliquot transfers from 15 and 50ml tubes to 0.5ml tubes in a custom rack. Accurate height tracking based on user-input starting volumes for each reagent tube ensures that the pipette will not submerge in reagent and become contaminated. **Begin the protocol with 30 empty reagents tubes loaded in the custom 3x6 racks in slots 1 and 2 loaded down each row before across each column. The user is prompted to replace tubes throughout the protocol.** For reagent setup, see 'Additional Notes' below.

---

You will need:
* [Opentrons P1000 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 1000ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Sarstedt 15ml tubes # 62.554.502](https://www.sarstedt.com/en/products/diagnostic/urine/tubes/product/62.554.502/)
* [Sarstedt 50ml tubes # 62.547.004](https://www.sarstedt.com/en/products/laboratory/reagent-centrifuge-tubes/tubes/product/62.547.004/)
* Custom 3x6 tube rack for 0.5ml tubes with lid holders
* [Sarstedt 0.5ml tubes # 72.730.105](https://www.sarstedt.com/en/products/laboratory/screw-cap-micro-tubes-reaction-tubes/screw-cap-micro-tubes/product/72.730.105/)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* Plasma
* Serum
* CSF

## Process
1. Input the starting volumes (in ml) of each reagent tube.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 500ul of CSF is transferred from the first CSF tube to each of 30 0.5ml tubes using the same tip.
8. The user is prompted to replace the tubes with 20 new tubes.
9. 250ul of CSF is transferred from the second CSF tube to each of 20 0.5ml tubes using the same tip.
10. The user is prompted to replace the tubes with 30 new tubes.
11. 250ul of plasma is transferred from the plasma tube to each of 30 0.5ml tubes using the same tip.
12. The user is prompted to replace the tubes with 15 new tubes.
13. 250ul of serum is transferred from the plasma tube to each of 15 0.5ml tubes using the same tip.

### Additional Notes
Tube setup in 15-50ml rack adapter:  
* Plasma (15ml): rack well A1
* Serum (15ml): rack well A2
* CSF tube 1 (50ml): rack well A3
* CSF tube 2 (50ml): rack well A4

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
WVg09yfR  
1598

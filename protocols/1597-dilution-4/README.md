# Cell Culture Dilution 4: MS2 100, 1000x

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
This protocol performs the second of four cell culture dilutions (100 and 1000x) for MS2 E. coli reagent. **Please fill all 15ml reagent tubes to 10ml to ensure accurate height tracking throughout the liquid transfers.** For reagent setup , see 'Additional Notes' below.

---

You will need:
* [P1000 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [1000µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 15ml Falcon tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* PBS
* 15597 E. coli

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. 9ml from PBS tube in tuberack well A3 is transferred to mix tube 1 in tuberack well A2.
7. Step 6 is repeated 2x more for PBS tube in wells A4 and A5 to mix tubes 2 and 3 in wells B2 and C2, respectively.
8. 100ul of E. coli reagent is directly transferred to wells B3, B4, B5, C3, C4, and C5.
9. Using a new tip, 1ml of MS2 reagent is transferred to mix tube 1 in tuberack well A2.
10. Using the same tip from step 8, the contents of mix tube 1 are mixed 5x to create 10x dilution.
11. 1ml from mix tube 1 are transferred to mix tube 2 in tuberack well B2.
12. Using the same tip from step 10, the contents of mix tube 2 are mixed 5x to create 100x dilution.
13. 500ul of 100x diluted MS2 is transferred from mix tube 2 to each of the 3 tubes in tuberack wells B3, B4, and B5.
14. 1ml of 100x diluted MS2 is transferred to mix tube 2 to mix tube 3 in tuberack well C2.
15. The contents of mix tube 3 are mixed 5x to create 1000x dilution.
16. 500ul of 1000x diluted MS2 reagent is transferred from mix tube 3 to each of the 3 tubes in tuberack wells B3, B4, and B5.

### Additional Notes
Reagent tube setup:
![tube setup](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1597-dilution4/reagent_setup_new.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
81VgY2ck
1597

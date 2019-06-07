# Cell Culture Dilution 2: Coliform and HPC 100, 1000x

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
This protocol performs the second of four cell culture dilutions (100 and 1000x) for Coliform and HPC reagent. **Please fill all 15ml reagent tubes to 10ml to ensure accurate height tracking throughout the liquid transfers.** For reagent setup , see 'Additional Notes' below.

---

You will need:
* [P1000 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [1000µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [SPL 6-Well Culture Plate](https://www.amazon.com/gp/product/B01DHK4YM4/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 15ml Falcon tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* PBS
* Coliform and HPC

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. 9ml from PBS tube in tuberack well A2 is transferred to mix tube 1 in tuberack well A1.
7. Step 6 is repeated 2x more for PBS tube in wells B2 and C2 to mix tubes 2 and 3 in wells B1 and C1, respectively.
8. Using a new tip, 1ml of Coliform and HPC reagent is transferred to mix tube 1 in tuberack well A1.
9. Using the same tip from step 8, the contents of mix tube 1 are mixed 5x to create 10x dilution.
10. Using a new tip, 1ml from mix tube 1 are transferred to mix tube 2 in tuberack well B1.
11. Using the same tip from step 10, the contents of mix tube 2 are mixed 5x to create 100x dilution.
12. 500ul of 100x diluted Coliform and HPC reagent is transferred from mix tube 2 to each of the 3 wells in row A of the 6-well plate.
13. Using a new tip, 1ml of 100x diluted Coliform and HPC reagent is transferred to mix tube 2 to mix tube 3 in tuberack well C1.
14. Using the same tip from step 13, the contents of mix tube 3 are mixed 5x to create 1000x dilution.
15. 500ul of 1000x diluted Coliform and HPC reagent is transferred from mix tube 3 to each of the 3 wells in row B of the 6-well plate.

### Additional Notes
Reagent tube setup:  
![tube setup](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1597-dilution2/tube_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
81VgY2ck  
1597

# Dreamtaq Standard Colony PCR Preparation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs a PCR preparation with DreamTaq mastermix and E coli colonies. The preparation is done on a PCR strip seated in an aluminum block on the OT-2 temperature module. During the process, a second PCR strip with suspended E coli colonies is produced for later use and does not receive PCR mastermix. For proper reagent setup on a 4x6 tube rack, see the 'Additional Notes' section below.

---

You will need:
* [PCR strips](https://uk.vwr.com/store/catalog/product.jsp?catalog_number=732-1517)
* [4x6 Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [1.5ml Microfuge Tubes](https://www.fishersci.co.uk/shop/products/product/11558232)
* [10µl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Aluminum block set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)

### Reagents
* [Thermo EP0701 DreamTaq DNA polymerase](https://www.thermofisher.com/order/catalog/product/EP0701)
* [Thermo EP0701 DreamTaq 10x PCR buffer](https://www.thermofisher.com/order/catalog/product/EP0701)
* [Thermo R0241 2mM dNTPs](https://www.thermofisher.com/order/catalog/product/R0241?SID=srch-srp-R0241)
* Thermo nuclease-free H2O

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. The temperature module is cooled to 4˚C.
7. The overall mastermix is prepared by transferring the proper ratios of nuclease-free H2O, primer 1, primer 2, DreamTaq buffer, dNTP, and DreamTaq polymerase to an empty microfuge tube. 10x the specified volumes of each reagent needed for each sample is transferred to the mix to ensure accommodation of 8 PCR samples on the PCR strip.
8. The completed mastermix is mixed 10x at maximum pipette volume.
9. A user-specified volume of nuclease-free H2O is transferred to each well of the PCR strip. Note that the final volume of H2O in each well will be half the specified volume. (See step 11.)
10. The program pauses and prompts the user to remove the PCR strip to pipette a single E. coli colony to each well and resuspend the colony. Replace the strip along with a second empty strip in column 2 of the aluminum PCR block.
11. Half of the H2O volume of each well is transferred to the adjacent well on strip 2, which will later be removed for refrigeration storage. Fresh tips are used for each transfer.
12. The mastermix is distributed to each well of strip 1. The volume to be transferred to each well is calculated by summing the input volumes of H2O, primers 1 and 2, dNTP, and DreamTaq buffer and polymerase.

### Additional Notes
![4x6 Tube Rack Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1512-isomerase-theapeutics/tube_setup.png)

###### Internal
qZn4HYNB  
1512

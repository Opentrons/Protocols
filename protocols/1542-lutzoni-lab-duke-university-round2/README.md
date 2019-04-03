# PCR Preparation Part 2/2

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs the second of two rounds of PCR preparation for 96 samples. For reagent tube and deck slot setup, please see the Additional Notes section below.

---

You will need:
* [Eppendorf PCR coolers](https://online-shop.eppendorf.com/OC-en/Temperature-Control-and-Mixing-44518/Accessories-44520/PCR-Cooler-PF-55940.html)
* [Olympus 96-well Plate](https://geneseesci.com/shop-online/product-details/24-300)
* [VWR 1.7ml Microcentrifuge Tubes](https://us.vwr.com/store/product/4674082/vwr-supercleartm-microcentrifuge-tubes-polypropylene)
* [Opentrons 10ul Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300ul Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons P10 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5978988707869)
* [Opentrons P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [Platinum Taq Polymerase](https://www.thermofisher.com/order/catalog/product/10966026)

## Process
1. Specify the number of primers that will be used.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Master mix is made from buffer, dNTP, taq polymerase, BSA, and H2O. 50 samples worth of master mix is made in one tube, and 50 samples worth in another to account for greater volume than one tube can hold.
8. The master mix is mixed after all reagents are combined to ensure homogeneity.
9. 23ul is distributed from the first master mix tube to each of the first 48 wells of the second round PCR plate, and 23ul from the second master mix tube to each of the second 48 wells of the second round PCR plate.
10. PacBio barcode primer is transferred to all corresponding wells in the second round PCR plate.
11. PCR product from round one is transferred to all corresponding wells in the second round PCR plate.

### Additional Notes
![Deck Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1542-lutzoni-lab-duke-university-round2/deck_setup.png)

![Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1542-lutzoni-lab-duke-university-round2/reagent_tube_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
yUHtcXcg  
1542

# CSV Sample Dilution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
This protocol performs sample dilutions in H2O across multiple deepwell plates. The user can specify 20x, 100x, 200x, or 400x dilutions in H2O via CSV. The final dilution carried out on a flat culture plate is 10x in HCl for all samples. Any other inputs (good practice to enter `Empty` in the CSV) will be ignored during parsing. The input CSV dilution information should start at the first value of the CSV, and be laid out in 8 row x 12 column format-- see 'Additional Notes' below for formatting details.

---

You will need:
* [Greiner Masterblock 96-deepwell plates # 780270](https://shop.gbo.com/en/usa/products/bioscience/microplates/polypropylene-storage-plates/96-well-masterblock-2ml/780270.html)
* [Nunc 96-Well Polypropylene Storage Microplates # 249946](https://www.thermofisher.com/order/catalog/product/249943)
* [Agilent single-channel reservoir # 201252-100](https://www.agilent.com/store/en_US/Prod-201252-100/201252-100)
* [Opentrons P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [300ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your CSV file and select the mount for your P300 pipette.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The dilution CSV is parsed for the dilution factor of each well. 20x and 100x dilutions are carried out in the corresponding wells of the source plate, 2 dilution plates, and the end culture plate, while 200x and 400x dilutions are carried out in the corresponding wells of the source plate, 3 dilution plates, and the end culture plate.

### Additional Notes
Example CSV:
![CSV layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1624/csv_layout.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
tWvf21LX  
1624

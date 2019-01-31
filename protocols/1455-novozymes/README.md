# MS Fraction Transfer Method

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Well-to-well Transfer

## Description
With this protocol, your robot can (1) transfer samples from a 96-well deep well Fraction Plate to HPLC vials, and (2) transfer samples from Fraction Plate to scintillation vials. The chosen wells in the fraction will be washed with water, and water will be added to the scintillation vials. Sample position origin and destination info will be uploaded as CSVs in the fields below. See Additional Information for more details.

---

You will need:
* P300 or P1000 Single-Channel Pipette
* [Greiner Bio-One 96-well MASTERBLOCK](https://shop.gbo.com/en/usa/products/bioscience/microplates/polypropylene-storage-plates/96-well-masterblock-2ml/780271.html)
* [Snap Top Autosampler Vials 475 uL](https://www.thermofisher.com/order/catalog/product/C4011-13)
* [Autosampler Vial Plate](https://www.agilent.com/store/en_US/Prod-G2255-68700/G2255-68700)
* [20 mL Glass Scintillation Vials with Attached Caps](http://www.kimble-chase.com/advancedwebpage.aspx?cg=728&cd=5&SKUTYPE=202&SKUFLD=SKU&DM=1250&WEBID=7412)
* Custom 4x2 Scintillation Vial plate
* 12-well Trough
* 300 uL Filter Tip Racks or 1000 uL Tips

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select your pipette and the pipette mount.
2. Upload HPLC and scintillation CSV.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will transfer samples from Fraction Plate to HPCL vials based on the HPLC CSV.
9. Robot will transfer samples from Fraction Plate to scintillation vials based on the scintillation CSV.
10. Robot will wash the sample source of the scintillation plate with 1 mL of water.
11. Robot will transfer the wash water to the scintillation plate based on the scintillation CSV.


### Additional Notes
Volume of each scintillation vial is capped at 10 mL. A second Scintillation vial/plate is placed in slot 6 to catch extra transfer volume (also capped at 10 mL).

---
CSV Examples:

![csv_example](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1455-novozymes/csv_example.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
vrAeMVZk
1455

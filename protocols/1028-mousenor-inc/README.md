# cAMP-Screen® 96-well Cyclic AMP Immunoassay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * ELISA

## Description
With this protocol, you robot can perform the cAMP-Screen Direct assay using the cAMP-Screen™ Cyclic AMP Immunoassay System from ThermoFisher. The cAMP-Screen assay systems are used for quantification of cellular cAMP for functional assays of receptor activation. Please make sure to read the Additional Notes at the bottom of this page and the [c-AMP-Screen and cAMP-Screen Direct System User Guide](https://assets.thermofisher.com/TFS-Assets/LSG/manuals/cms_039440.pdf) for more details on this protocol.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* [cAMP-Screen™ Cyclic AMP Immunoassay System](https://www.thermofisher.com/order/catalog/product/4412182?SID=srch-srp-4412182)

## Process
1. Set the starting column of samples in your source plate.
2. Set the number of columns on the plate that contain your samples (MAX = 10 columns).
3. Set the starting column on the assay plate, where your first standards column would be.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will incubate sample plate on TempDeck for 30 minutes at 37°C.
10. Robot will transfer assay/lysis buffer to each sample using a P300 multi-channel pipette.
11. Robot will incubate sample plate on TempDeck for 10 minutes at 37°C.
12. Robot will prepare cAMP standard in 96-deep well plate column 1.
13. Robot will transfer cAMP standard dilutions in duplicate on ELISA plate.
14. Robot will transfer sample + lysis buffer mixture in step 10 to the ELISA plate.
15. Robot will transfer diluted cAMP-AP to standards and samples on the ELISA plate.
16. Robot will transfer anti-cAMP antibody to standards and samples on the ELISA plate.
17. Robot will incubate the ELISA at room temperature for 60 minutes.
18. Robot will remove all solution from all wells on the ELISA plate.
19. Robot will wash the plate 6 times with wash buffer.
20. Robot will transfer CSPD/Sapphire-II RTU substrate/enhancer solution to standards and samples on the ELISA plate.
21. Robot will incubate the plate for 30 minutes at room temperature.

### Additional Notes
Setup
* ELISA Plate: slot 2
* Dilution Plate: slot 3
* Sample Plate on TempDeck: slot 4
* [12-row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx): slot 5
* [2-row Trough](http://www.eandkscientific.com/2-Column-Reservoir.html): slot 7

12-Row Trough Reagents
* cAMP Standard: A1
* Lysis Buffer: A2
* Diluted cAMP-AP Conjugate: A3
* Anti-cAMP Antibody: A4
* CSPD/Sapphire-II RTU Substrate/Enhancer Solution: A5

2-Row Trough Reagents
* Wash Buffer: A1
* Liquid Trash (leave empty): A2

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
kZu9rwl8
1028

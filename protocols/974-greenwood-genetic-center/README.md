# qPCR Protocol

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Sample Prep

## Description
With this protocol, your robot can perform qPCR for up to 4 assays, each with up to 4 patient samples. You need to upload each layout CSV before starting the protocol, as well as input the variables Ngoi, N1, and N2.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Upload your Layout CSV.
2. Input your desired Ngoi, N1, and N2.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. The robot will prepare the housekeeping master mix.
9. The robot will prepare the Gene of Interest 1 master mix.
10. The robot will prepare the Gene of Interest 2 master mix.
11. The robot will distribute the appropriate master mix into the wells in the 96-well plate according to the layout CSV.
12. The robot will then transfer samples to the appropriate wells according to the CSV.

### Additional Notes
* Reagent setup in the 2 mL tube rack:
    * A1:	Sybr green master mix (2x)
    * B1:	Forward primer 1 (10uM)
    * C1:	Reverse primer 1(10uM)
    * D1:	H2O
    * A2:	Template DNA (proband 1)
    * B2:	Template DNA (Mother 1)
    * C2:	Template DNA (Father 1)
    * D2:	Template DNA (Normal Control 1)
    * A3:	Template DNA (Normal Control 2)
    * B3:	Template DNA (Normal Control 3)
    * C3:	Template DNA (Normal Control 4)
    * D3:	TaqMan master mix (2x)
    * A4:	Housekeeping gene probe (20x)
    * B4:	Forward primer 2 (10uM)
    * C4:	Reverse primer 2(10uM)
    * D4:	Template DNA (proband 2)
    * A5:	Template DNA (Mother 2)
    * B5:   Template DNA (Father 2)
    * C5:   housekeep_master_mix [empty]
    * D5:   tube
    * A6:   tube

    
* Default CSV file format:
    ![CSV format](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/greenwoood_genetic_center_qpcr.png)


###### Internal
e0PgrHa5
974

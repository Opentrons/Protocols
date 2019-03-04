# DNA Dilution and PCR Preparation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs a DNA sample dilution and PCR preparation on a custom PCR loading block for 48 samples. The preparation is done on a PCR strip seated in an aluminum block on the OT-2 temperature module. The protocol allows for user input volumes of each reagent to be transferred to the PCR tubes. For proper PCR tube strip and reagent setup, see 'Additional Notes' below.  

  __Note__: Due to the dimensions of this custom plate, in order to conserve tips and avoid crashing, remove all tips from the the bottom two rows of the 10µl tip rack do not have tips inserted.

---

You will need:
* [Custom Mic SBS Loading Block](https://s3-ap-southeast-2.amazonaws.com/paperform/u-4256/0/2019-02-22/2u134ra/MIC-SBSLB-A.pdf)
* [0.2 mL 8-strip PCR tubes](https://www.nerbe-plus.de/ENU/21677/Item.aspx?FromNo=21676&ItemNo=04-032-0500)
* [4-strip qPCR Mic tubes](http://www.labgene.ch/mic-real-time-pcr-system/238-4-strip-tubes-with-caps-for-mic.html)
* [p10 8-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [p50 Single-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [Opentrons 10µl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300µl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [4x6 2ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [96-well Aluminum block](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set) (or equivalent for seating 8-strip PCR tubes)

### Time Estimate
30 minutes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Once the robot is calibrated and the main protocol is uploaded to the run app, the robot begins with DNA sample dilution. 2 PCR strips occupying rows A and B (6 wells each) in the aluminum block contain pure DNA sample. 2 strips occupying rows C and D (6 wells each) contain 18µl of water for dilution. 2µl from each well of row A are distributed to the corresponding wells in row C, and 2µl of row B are distributed to the corresponding wells in row D. This results in a 10x dilution from row A to C, and from row B to D.
7. The reaction mix preparation is prepared in a 1.5ml tube in the tube rack according to the user specified volumes of each reagent that will comprise each PCR sample (n=48). 52x each of these volumes is transferred to the mix tube to ensure enough volume for every PCR tube in the rack. The completed mix is mixed 3x after each reagent transfer to ensure homogeneity.
8. The mix is distributed to all of 48 tubes fully occupying the right rack of the custom block.
9. The DNA samples from the PCR strips are then transferred to the block with pre-added mix according the the schematic in 'Additional Notes' below.

### Additional Notes
![4x6 Tube Rack Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1507-department-of-protein-dna-interactions-institute-of-biotechnology/TubeRackSetup.png)  

![Sample Transfer Schematic](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1507-department-of-protein-dna-interactions-institute-of-biotechnology/TransferSetup.png)

###### Internal
RZJl8zTF  
1507

# Mass Spec Sample Prep on Custom Slide

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Assay

## Description
This protocol performs a mass spec sample prep on up to 63 samples on a custom 72-sample slide mount (the top row of 9 wells are left blank). Samples are taken from and filled in the slides down the columns, then across the rows. For more detailed sample and reagent setup, please see below.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* custom 3-grid 3x8 slide mount
* [Opentrons 4x6 tuberack insert](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1) with 1.5ml Eppendorf snapcap tubes
* [Opentrons 2x3 tuberack insert](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1) with 50ml Falcon tubes
* [Opentrons 20ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips?variant=15954632802398)
* [Opentrons P20- and P300-single GEN2 electronic pipettes](https://shop.opentrons.com/collections/ot-2-pipettes)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

2x3 50ml tuberack (slot 1)
* detergent wash buffer: tube A1
* BSA blocking buffer: tube B1
* PBS: tubes A2-B2
* water: tubes A3-B3

sample rack 1 (slot 9):
* tube A1: sample 1
* tube B1: sample 2
* ...
* tube A2: sample 5
* ...
* tube D6: sample 24

sample rack 2 (slot 6):
* tube A1: sample 25
* tube B1: sample 26
* ...
* tube A2: sample 29
* ...
* tube D6: sample 48

sample rack 3 (slot 3):
* tube A1: sample 49
* ...
* tube D3: sample 63
* **tube D6: antibody**

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the number of samples, and the respective mount sides for your P20 and P300 pipettes.
2. Download your protocol package.
3. Upload your custom labware and protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2). **Ensure that you calibrate your slides mounted on the Teleshake to the precise location from which you would like to aspirate liquid.**
6. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
51df08

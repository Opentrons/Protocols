# PCR Prep

### Author
[Opentrons](https://opentrons.com/)


# Opentrons has launched a new Protocol Library. This page won’t be available after March 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* PCR
	* PCR Prep

## Description

This protocol performs a custom PCR prep by transferring samples, primers, BigDye, and water to a clean PCR plate. New tips are used for each transfer, both to avoid contamination and to accurately dispense small volumes (1-6µl). See below for deck and reagent setups.

Note that the product of the number of samples multiplied by the number of primers cannot exceed 96, or an exception will be thrown.

An example of the transfer scheme is shown in the following schematic:  
![scheme](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/69cf81/scheme.png)

---

### Labware
* [ThermoFisher MicroAmp™ Optical 96-Well Reaction Plate with Barcode #4306737](https://www.thermofisher.com/order/catalog/product/4306737#/4306737)
* [NEST 15 Reservoir 12ml](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)
* [Opentrons 20µl Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips) or [Rainin 20µl Tipracks](https://www.shoprainin.com/Products/Pipettes-and-Tips/Pipette-Tips/LTS-Pipette-Tips/SpaceSaver/Pipette-Tips-GPS-LTS-20µL-S-960A-10/p/30389297)

### Pipettes
* [P20 8-Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)

### Reagents
* BigDye

---

### Deck Setup
The following example shows a setup for 16 samples and 6 primers. Note that samples can continue across the plate, and primers can continue down and then across the tuberack.  
* green in reagent reservoir: unique primer, BigDye + water mix
* blue in sample plate: PCR templates
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/69cf81/deck2.png)

---

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
69cf81

# Nucleic Acid Extraction

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
This protocol performs nucleic acid extraction on a sample plate mounted on an Opentrons magnetic module. The protocol allows for the user to select the number of sample columns to be processed. For reagent, refer to 'Additional Information' below.

---

You will need:
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [15ml Tube rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [MidSci 96-well Non-skirted PCR plate #B70501](http://shop.midsci.com/productdetail/M50/B70501/EU_PCR_Plate,_96x0.2ml,_Non-Skirted,_Natural,_Regular_Profile,_25/cs/)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* [Wizard magnetic 96 DNA plant system, promega](https://us.vwr.com/store/product/23398197/wizard-magnetic-96-dna-plant-system-promega)

## Process
1. Input the number of sample columns you would like to process.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 60ul of buffer B is transferred to each well to be processed on the plate mounted on the magnetic module. The contents of the well are mixed 15x after the transfer, and new tips are used for each transfer and mix sequence.
8. The protocol pauses for the samples to incubate for 3 minutes.
9. The contents of each well from step 7 are mixed 10x. New tips are used for each mix.
10. The protocol pauses for the samples to incubate for 2 minutes.
11. The magnetic deck engages, and the samples incubate for 1 minute and 30 seconds.
12. The magnetic deck disengages, and wash buffer is transferred to each sample. The samples are mixed 15x after the transfer, and new tips are used for each transfer and mix sequence.
13. The magnetic deck engages, and the samples incubate for 1 minute and 30 seconds.
14. Supernatant is discarded in the liquid waste reservoir.
15. Steps 12-14 are repeated 1x for a total of 2 washes.
16. The samples incubate for 6 minutes, and the magnetic deck disengages.
17. 50ul of nuclease-free H2O is transferred to each sample. The samples are mixed 15x after the transfer, and new tips are used for each transfer and mix sequence.
18. The samples incubate for 5 minutes, and the magnetic deck engages.
19. The samples incubate for 1 minute and 30 seconds.
20. 45ul of each sample is transferred from the plate on the magnetic deck to its corresponding location on a fresh plate. Different tips are used for each transfer.

### Additional Notes
![Reagent Setup in 12-row Trough](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1584/reagent_setup_in_trough.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
A6iloAlf  
1584

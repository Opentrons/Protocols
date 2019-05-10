# CSV PCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs PCR preparation on a SSBio strip tubes seated in a Perkin Elmer 384-well view plate. Ensure that strip tubes are arranged down each column of the plate before moving across each row, and that the plate is filled with enough tubes to accommodate the number of lines in the input CSV. Transfers are carried out according to this CSV for both knockdowns (1ul per transfer) and primers (9ul per transfer). See Additional Notes below for reagent setup.

---

You will need:
* [Perkin Elmer 384-Well View Plate](http://www.perkinelmer.com/lab-products-and-services/application-support-knowledgebase/microplates/plate-dimensions.html#Microplatedimensionsworkingvolumespackagingandphotos-ViewPlate)
* [SSBio Corbett-Type Strip Tubes and Caps #3188-00](http://www.ssibio.com/pcr/strip-pcr-tubes-and-caps/corbett-type-strip-tubes-and-caps/3188-00)
* [Opentrons 2ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 1.5ml Eppendorf Tubes
* [Opentrons 10ul Tips](https://www.usascientific.com/tiponefiltertips.aspx)
* [Opentrons P10 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [MESA GREEN qPCR MasterMix Plus for SYBR Assay](https://secure.eurogentec.com/product/research-mesa-green-qpcr-mastermix-plus-for-sybr-assay.html)

## Process
1. Upload your input CSV file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol parses the CSV to determine which primer will be transferred to each destination strip tube. 9ul of the appropriate primer is transferred to the destination tube. The volume is blown out and the pipette touches tip after each transfer, and a new tip is used for each transfer.
8. The protocol parses the CSV to determine which knockdown will be transferred to each destination strip tube. 1ul of the appropriate knockdown is transferred to the destination tube. The volume is blown out and the pipette touches tip after each transfer, and a new tip is used for each transfer.

### Additional Notes
![Eppendorf Tube Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1530-university-of-bern/reagent_setup.png)
Please note that 'Knockdown' reagents are shown in red, and 'Primer' reagents are shown in blue.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
DsfNO5wD  
1530

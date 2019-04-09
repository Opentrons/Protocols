# PCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs PCR preparation on a custom 96-well PCR plate for a specified number of DNA samples and oligo standards. All samples are carried out in triplicate. To see diagrams for initial and second reagent setup, as well as triplicate filling order, see Additional Notes below.

---

You will need:
* [BioRad 96-Well PCR plate](http://www.bio-rad.com/en-us/sku/mll9651-multiplate-96-well-pcr-plates-low-profile-unskirted-white?ID=MLL9651)
* [Opentrons 2ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Diamed 2ml Microfuge Tubes](http://www.diamed.ca/microcentrifuge-tubes-15ml-microtubes-bulk-c-265_496_497.html)
* [Fisherbrand 1.5ml Microfuge Tubes](https://www.fishersci.com/shop/products/fisherbrand-low-retention-microcentrifuge-tubes-8/p-193936)
* [TipOne 10ul Tips](https://www.usascientific.com/tiponefiltertips.aspx)
* [TipOne 50ul Tips](https://www.usascientific.com/tiponefiltertips.aspx)
* [Opentrons P10 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons P50 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents
* [Bio-Rad SsoAdvanced Universal SYBR Green Supermix](http://www.bio-rad.com/en-ca/product/ssoadvanced-universal-sybr-green-supermix?ID=MH5H1EE8Z)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. 15ul of master mix are distributed to each well of the 96-well plate, which is loaded on the temperature module.
7. 5ul of each of the specified number of DNA samples is transferred to its corresponding set of 3 destination wells according to the plate diagram in Additional Notes below.
8. To avoid contamination, the protocol pauses and prompts the user to replace the master mix and DNA sample tubes with oligo standard tubes, positive control tube, and NTC tube according to the reagent setup diagrams in Additional Notes below.
9. 5ul of positive control is transferred to its corresponding set of 3 destination wells according to the plate diagram in Additional Notes below.
10. 5ul of NTC is transferred to its corresponding set of 3 destination wells according to the plate diagram in Additional Notes below.
11. 5ul of each of the specified number of oligo standards is transferred to its corresponding set of 3 destination wells according to the plate diagram in Additional Notes below.

### Additional Notes
![Initial Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1552-contango-strategies-ltd/reagent_setup_1.png)

![Second Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1552-contango-strategies-ltd/reagent_setup_2_.png)

![Transfer Diagram](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1552-contango-strategies-ltd/transfer_diagram.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
nU8R1Kic  
1552

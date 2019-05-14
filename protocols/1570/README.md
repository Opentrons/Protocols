# NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library prep for a user-selected number of samples mounted on a temperature module.

---

You will need:
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [P10 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Axygen 96-well full-skirted PCR plate](https://ecatalog.corning.com/life-sciences/b2c/US/en/Genomics-&-Molecular-Biology/PCR-Consumables/PCR-Microplates/Axygen%C2%AE-96--and-384-well-PCR-Microplates-and-Sealing-Mats-for-0-2-mL-Thermal-Cycler-Blocks/p/PCR-96-FS-C)
* Rainin pipette tips
* [2ml Tube rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module with 96-well aluminum block](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents
* [iGenomX Riptide](https://igenomx.com/product/riptide/)

## Process
1. Input your number of sample columns and volume of DNA to pool at the end of the protocol.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol waits for the temperature deck to reach 4˚C.
8. 2ul of barcode is transferred to the corresponding well of the plate mounted on the temperature module.
9. 6ul of master mix is transferred to each sample of the plate mounted on the temperature module.
10. 2ul of DNA sample is transferred to the corresponding well of the plate mounted on the temperature module. Contents are mixed after each transfer.
11. The protocol pauses for the user to perform a reaction.
12. A specified volume of all DNA samples are pooled from their source plate into a tube containing EDTA.

### Additional Notes
![Tube Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1570/tube_setup.png)

![Deck Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1570/deck_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
GndpqbLC  
1570

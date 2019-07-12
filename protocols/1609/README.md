# NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library prep on a PCR plate mounted on an Opentrons magnetic module. Due to limited deck space, the user will be prompted to refill tipracks on the deck when necessary. For reagent setup, see Additional Notes below.

---

You will need:
* [Greiner Sapphire PCR strips # 673273](https://shop.gbo.com/en/usa/products/bioscience/molecular-biology/thin-wall-pcr-tubes/pcr-8-tube-strips/673273.html)
* [Greiner 96 well PCR plate - skirted # 652270](https://www.sigmaaldrich.com/catalog/product/sigma/z711063?lang=en&region=US)
* [USA Scientific 12-channel reservoir # 1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons P10 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons P300 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons Temperature Module with mounted 96-well aluminum block](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents
* [Illumina Nextera flex kit](https://www.illumina.com/products/by-type/sequencing-kits/library-prep-kits/nextera-dna-flex.html)
* MQ
* 80% EtOH (freshly prepared)
* [CleanNGS beads](http://www.cleanna.com/cleanngs)

## Process
1. Input the number of sample columns to be processed (up to 6) and the start column for the index plate.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
Tempdeck-mounted PCR strips setup (deck slot 4):
* BLT: strip 1 (all 8 tubes)
* TB1: strip 2 (all 8 tubes)
* CleanNGS beads: strip 3 (all 8 tubes)

Non-tempdeck-mounted PCR strips setup (deck slot 5):
* TSB: strip 1 (all 8 tubes)
* EPM: strip 2 (all 8 tubes)

12-Channel trough setup:
* MQ: channel 1
* TWB: channel 2
* 80% EtOH: channels 3-4
* EB/resuspension buffer: channel 5
* liquid waste: channel 12 (starts empty)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
IKfeZJAN  
1609

# Cell Culture Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Cell Culture
    * Assay

## Description
This protocol performs a cell culture assay on custom 96-well plates. Reagents are contained in 50ml Falcon tubes. Please see 'Additional Notes' below for reagent tube setup. Ensure that reagents are filled to the 50ml line of the tubes for accurate height tracking.

---

You will need:
* [P50 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [TipOne 300µl Pipette Tips](https://www.usascientific.com/300ul-tipone-rpt-filtertip.aspx)
* [TipOne 100µl Pipette Tips](https://www.usascientific.com/100ul-tipone-rpt-profile-filter-tip.aspx)
* [Corning 96-Well TC-Treated Microplates](https://www.sigmaaldrich.com/catalog/product/sigma/cls3596?lang=en&region=US)
* [50ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 50ml Falcon Tubes
* 96-well Flat PCR Plate

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* Cell media
* PBS
* Trypsin

## Process
1. Upload your file, and select the input values for P and T.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The robot will execute the cell assay split. The name of the written file will be displayed in the Run App after the protocol finishes (Note-- the file is written only in the case that P = 'no').

### Additional Notes
![Tube Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1566/reagent_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
YETERTsD  
1566

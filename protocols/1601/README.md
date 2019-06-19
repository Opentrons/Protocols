# Mass Spec Sample Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Mass Spec

## Description
This protocol performs mass spec sample preparation for up to 50 samples on two 10x5 tube racks. Reagents are held in 15ml tubes; **to ensure accurate height tracking, fill each 15ml reagent tube to ~2cm below the opening of the tube**. To see diagrams for reagent setup, see 'Additional Notes' below.

---

You will need:
* [Mercedes Medical 50x Vial Racks # MER VR1001](https://www.mercedesmedical.com/default.aspx?page=item%20detail&itemcode=MER+VR1001)
* [Opentrons 15ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 3ml false-bottom tubes
* [Thomson Instrument Company Filter Vials, VWR catalog # 101447-036](https://us.vwr.com/store/product/18556015/standard-filter-vials-thomson-instrument-company)
* [Opentrons P30 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* Globe Scientific 200ul pipette tips

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount for your P300 pipette and the number of samples to be processed.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 50ul of mastermix is transferred to each specified filter vial in the second tuberack.
8. 50ul of each sample in false bottom tubes in the first rack is transferred the corresponding filter vial in the second rack.
9. The protocol pauses and prompts the user to incubate the filter vials, now containing mastermix and samples.
10. 300ul of diluent is transferred to each specified filter vial in the second tuberack.

### Additional Notes
15ml tube rack setup:
* mastermix: tube A1 **(filled to ~2cm below the opening of the tube)**
* diluent: tube B1 **(filled to ~2cm below the opening of the tube)**

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
T9xcPtRu  
1601

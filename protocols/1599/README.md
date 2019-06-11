# Customizable Cell Culture Serial Dilution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Serial Dilution

## Description
With this protocol, you can perform a cell culture serial dilution across a 96-well plate. **Ensure the diluent tube in well A1 of the 15ml tube rack is filled to ~14ml to ensure accurate height tracking throughout the protocol.** For reagent setup, see 'Additional Notes' below.

---

You will need:
* [Greiner Bio-One 96-well plate # 655161](https://shop.gbo.com/en/england/products/bioscience/microplates/96-well-microplates/96-well-microplates-clear/655161.html)
* Tip One 50 and 300ul pipette tips
* [Greiner 15ml centrifuge tubes # 188261](https://shop.gbo.com/en/england/products/bioscience/tubes-beakers/tubes/15ml-cellstar-polypropylene-tube/)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input your dilution factor, total mixing volume, number of samples, number of dilutions per sample, dilution start well (in format 'row + column', ex: 'A1'), dilution orientation, and tip use strategy (per each sample's dilution).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The serial dilution is carried out on the Greiner 96-well plate according to the input parameters.

### Additional Notes
Reagent setup in 15ml tube rack:
* diluent: tube A1 (filled to ~14ml)
* liquid_trash: tube B1 (loaded empty)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
u39J5AjU  
1599

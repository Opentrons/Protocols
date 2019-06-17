# PCR Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs PCR preparation on 4 custom 96-well PCR plates. DNA samples are contained in a PCR plate mounted on an aluminum block on an Opentrons temperature module. For reagent setup, see 'Additional Notes' below.

---

You will need:
* [BioRad low-profile 96-well PCR plates # hsp9601](http://www.bio-rad.com/en-us/sku/mll9651-multiplate-96-well-pcr-plates-low-profile-unskirted-white?ID=MLL9651)
* [USA Scientfic 12-channel reservoir for automation # 1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons 10ul Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300ul Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons P10 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons P50 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons Temperature Module with 96-well aluminum block](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Input your number of sample columns to be processed.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The temperature module with DNA samples mounted cools to 4˚C. The program resumes after the temperature is reached.
8. 22ul of mastermixes 1-4 in the 12-channel trough are distributed to each specified sample column of PCR plates 1-4, in slots 2, 3, 5, and 6, respectively. Tips are refreshed for each mastermix.
9. 3ul of DNA sample is transferred to its corresponding well in each of the 4 PCR plates. Contents are mixed 5x and tips are changed after each transfer.

### Additional Notes
12-channel trough setup:  
* Mastermix 1: channel 1
* Mastermix 2: channel 2
* Mastermix 3: channel 3
* Mastermix 4: channel 4

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
EkBu99wv  
1605

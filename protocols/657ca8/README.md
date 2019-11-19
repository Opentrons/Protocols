# DNA Normalization

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* DNA Normalization

## Description
This protocol performs a custom DNA normalization specified in `.csv` file from 2ml source tubes (aligned in up to 4 4x6 racks) to 0.5ml destination tubes (aligned in 8x12 racks). The DNA is normalized to 125ul total using TE buffer from a 15ml centrifuge tube as diluent; the aspiration height from the tube is automatically calculated to avoid pipette submersion in the buffer. The `.csv` file should be uploaded in the following format (**including the initial header line**):

```
PtID,Source rack (1-4),Source well,Destination well,DNA (ul), water (ul)
10013393,1,A01,A01,50,75
10012852,2,A02,A02,41,84
10013300,1,A03,A03,46,79
10013324,1,A04,A04,41,84
10012592,1,A05,A05,40,85
10012378,1,A06,A06,62,63
10012541,1,B1,A07,55,70
10012189,1,B2,A08,53,72
```

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Fisherbrand 2ml microcentrifuge screwcap tubes #02-682-558](https://www.fishersci.com/shop/products/fisherbrand-free-standing-microcentrifuge-tubes-screw-caps-3/p-3251083) seated in up to 4 [Opentrons 4-in-1 tuberacks with 4x6 2ml tube inserts](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Thermo Scientific 0.5ml matrix screwcap tubes seated in 96-tube latch rack #3744](https://www.thermofisher.com/order/catalog/product/3743AMB-BR#/3743AMB-BR)
* [NEST 15 mL centrifuge tube](https://shop.opentrons.com/collections/verified-consumables/products/nest-15-ml-centrifuge-tube) (or equivalent) seated in [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1) with 3x5 15ml tube insert
* [Opentrons GEN1 P300 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons 300ul tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

3x5 15ml tuberack (slot 6)
* tube A1: buffer

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P300 single-channel pipette, and upload your `.csv` file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
657ca8

# SNP Genotyping

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
With this protocol, your robot can prepare SNP Genotyping assay using the [TaqMan® Genotyping Master Mix](https://www.thermofisher.com/order/catalog/product/4371355) on a 384-well plate. The plate layout will be input by user in the CSV format in the upload field below. See Additional Notes at the bottom of this page for more details on the CSV setup.

---

You will need:
* P10 Single-channel Pipette
* P50 Single-channel Pipette
* [Opentrons 4-in-1 Tube Rack Sets](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [96-well PCR plate, low profile, skirted ](https://www.thermofisher.com/order/catalog/product/AB0800)
* [MicroAmp™ EnduraPlate™ Optical 384-Well Clear Reaction Plate](https://www.thermofisher.com/order/catalog/product/4483285)
* 10 uL Tip Racks
* 100 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* [TaqMan™ Genotyping Master Mix](https://www.thermofisher.com/order/catalog/product/4371355)

## Process
1. Upload your layout CSV.
2. Set the number of mixes and the volume of each mixing step to be performed after dispense the master mix to each well.
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will create the master mixes by first distributing Taqman Master Mix and then samples in either the 96-PCR plate (A1-H12) or 2 mL tubes succeeding the sample tubes.
9. Robot will then follow the CSV layout to transfer and mix the master mixes to their corresponding destination wells in the 384-well plate.

### Additional Notes
Layout CSV:

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1493-clinical-pharmacology-analytical-laboratory-jhu/layout.png)

* 24 columns x 16 rows
* Each cell represents a well in the 384-well plate
* An empty cell or a cell containing `0` means no master mix will be dispense in to the corresponding well
* Each number represents the master mix that should be transferred to that well

---

Tube Racks Layout:
* Taqman Master Mix: Tube Rack slot 1, well A1
* Samples: start at Tube Rack slot 1, well B1, C1, D1 ... D6,  then continue at Tube Rack slot 4 well A1...
* Right after the samples, place empty tubes in the tube rack for master mixes exceeding 200 uL

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
zlKPUJJa
1493

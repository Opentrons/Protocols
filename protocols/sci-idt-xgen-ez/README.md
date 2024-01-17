# IDT xGEN EZ

### Author
[Opentrons](https://opentrons.com/)


# Opentrons has launched a new Protocol Library. This page won’t be available after March 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* NGS Library Prep
	* IDT xGEN EZ

## Description
This protocol performs the [IDT xGEN EZ kit](https://sfvideo.blob.core.windows.net/sitefinity/docs/default-source/protocol/xgen-dna-library-prep-ez-kit-and-xgen-dna-library-prep-ez-uni-kits-protocol.pdf?sfvrsn=57b1e007_8). This protocol uses the stubby adapter (Reagent W5) that is included in the xGEN EZ kit during ligation and the barcoding of samples is performed during PCR by using either xGEN UDIs or CDIs.  The alternate protocol version is IDT xGEN EZ UNI that does the barcoding of samples at ligation instead.  The Protocol steps and reagents are different between the two versions.  See IDT’s xGEN DNA Library Prep EZ Kit protocol for more information about sample barcode kit requirements.

Explanation of complex parameters below:
* `Number of Samples`: Samples are prepared as pictured below; with 100ng of input DNA in 50ul of Low EDTA. See IDT’s xGEN DNA Library Prep EZ Kit protocol for more information about sample input requirements.
![samples1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.19.24+AM.png)
![samples2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.19.16+AM.png)
* `Fragmentation Time (minutes)`: Minutes, Duration of the Fragmentation Step
* `PCR Cycles`: Specify number of PCR cycles if performing PCR on deck.
* `Dry Run`: Yes will return tips, skip incubation times, shorten mix, for testing purposes.
* `Use Modules?`: Yes will not require modules on the deck and will skip module steps, for testing purposes, if `Dry Run` is set to `Yes`, then this variable will automatically set itself to `No`.
* `Reuse Tips?`: No, NYI format for reusing tips
* `Use protocol specific z-offsets?`: Sets whether to use protocol specific z offsets for each tip and labware or no offsets aside from defaults
* `Include Fragmentation / End-Repair / A-Tailing Step?`: Specify whether to include this step below. This and all steps below allow you to customize where to start the protocol, run the protocol in parts over multiple days, choose whether to use Opentrons modules or off deck modules, etc.
* `If yes, Fragmentation / End-Repair / A-Tailing on deck or off deck?`: Use this step on or off the deck.
* `Include Ligation Step?`: Specify whether to include this step in this run.
* `If yes, ligation Step on or off deck?`: Use this step on or off the deck.
* `Include Post Ligation Step?`: Specify whether to include this step in this run.
* `Include PCR Step?`: Specify whether to include this step in this run.
* `If yes, PCR step on or off deck?`: Use this step on or off the deck.
* `Include First Post PCR Step?`: Specify whether to include this step in this run.
* `Include Second Post PCR Step?`: Specify whether to include this step in this run.
* `P20 Multi-Channel Mount`: Specify which mount (left or right) to mount the P20 multi-channel pipette.
* `P300 Multi-Channel Mount`: Specify which mount (left or right) to mount the P300 multi-channel pipette.

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Thermocycler Module](https://shop.opentrons.com/collections/hardware-modules/products/thermocycler-module)

### Labware
* [NEST 0.1 mL 96-Well PCR Plate, Full Skirt](https://shop.opentrons.com/nest-0-1-ml-96-well-pcr-plate-full-skirt/)
* [* [NEST 0.1 mL 96-Well PCR Plate, Full Skirt](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* [NEST 2 mL 96-Well Deep Well Plate, V Bottom](https://shop.opentrons.com/nest-2-ml-96-well-deep-well-plate-v-bottom/)
* [Opentrons Aluminum Block Set](https://shop.opentrons.com/aluminum-block-set/)
* [Opentrons 20µL Filter Tips](https://shop.opentrons.com/opentrons-20ul-filter-tips/)
* [Opentrons 200µL Filter Tips](https://shop.opentrons.com/opentrons-200ul-filter-tips/)

### Pipettes
* [P20 Multi-Channel Pipette](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [P300 Multi-Channel Pipette](https://shop.opentrons.com/8-channel-electronic-pipette/)


---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.19.43+AM.png)

### Reagent Setup
* Prepare the reagents in the Reagent Plate according to the table below.  If available, prepare extra volume to  account for overage.  
![reagent plate](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.20.05+AM.png)
![reagent volumes](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.20.18+AM.png)
* This protocol is designed to be used with xGen UDI Barcode Primers.  Add 5ul of the appropriate Barcode adapter to column 7, 8, and 9 according to the experiment design.  See IDT xGEN EZ instructions for further details.  
![barcode table](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.20.39+AM.png)
* Fill the reservoir wells with the indicated volumes below.
![reservoir reagents](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.20.57+AM.png)
![reservoir volumes](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-idt-xgen-ez/Screen+Shot+2022-04-07+at+11.21.05+AM.png)
* Max Volume is 15ml, refill the EtOH reservoir after the first AMPure Cleanup.


---

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
sci-idt-xgen-ez

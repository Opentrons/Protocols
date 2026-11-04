# PCR Setup (1 to 53 reactions) with On-Deck Thermocycling, Recovered from a Video

### Author
Pugar Huda Mantoro, generated with [Show, Don't Code](https://github.com/PugarHuda/show-dont-code)

## Categories
* PCR
	* PCR Prep

## Description
This protocol assembles a 50 µL PCR in a 96-well PCR plate on the Thermocycler Module and then runs the cycling program on the deck, for 1 to 53 reactions. It was not written by hand: the steps and volumes were recovered from a first-person video of the same reaction being set up by a scientist (BioVL2 dataset, CC BY 4.0), then turned into this protocol by a deterministic code generator. Each step's comment names the seconds of video it came from, so it can be checked against the original side by side: https://show-dont-code.vercel.app/app?run=pcr_1-gt

Per reaction: 20 µL water, 1.5 µL Primer1, 1.5 µL Primer2, 2 µL template and 25 µL PrimeSTAR Max Premix, one new tip per transfer. Then 98 °C for 30 s; 35 cycles of 98 °C 10 s, 55 °C 5 s, 72 °C 5 s; hold at 4 °C with the lid open (heated lid at 105 °C while cycling).

Runtime parameters (set in the Opentrons App, no code changes):
* `Reactions`: copies of the reaction, filled down the plate's columns (A1, B1, ... H1, A2, ...). Tubes are filled for all of them.
* `Cycles` and every temperature and hold time of the program.

Checked with `opentrons analyze` (opentrons 9.0.0) at 1 and at 53 reactions (1,355 commands, no errors). Not yet run on a physical OT-2: do a water run first.

---

### Modules
* [Thermocycler Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/thermocycler-module) (slots 7, 8, 10, 11)

### Labware
* Opentrons 24 Tube Rack with Eppendorf 1.5 mL Safe-Lock Snapcap (slot 5)
* Opentrons 96 Well Plate 200 µL PCR Full Skirt (on the Thermocycler)
* Opentrons 96 Tip Rack 20 µL (slot 1; slots 2 and 3 above 24 reactions)
* Opentrons 96 Tip Rack 300 µL (slot 4)

### Pipettes
* P20 Single-Channel GEN2 (left)
* P300 Single-Channel GEN2 (right)

### Reagents
* PrimeSTAR Max Premix (2X)
* Primers and template of your choice

---

### Deck Setup
Tube rack in slot 5: A1 water, B1 Primer1, C1 Primer2, D1 template, A2 PrimeSTAR Max Premix. The App's Liquid Setup shows the volume to fill each tube for the chosen number of reactions (+10 % and 30 µL dead volume).

### Process
1. Import the protocol into the Opentrons App and set the number of reactions.
2. Fill the tubes as shown in Liquid Setup and open the caps.
3. Run Labware Position Check, then start the run.
4. After the run, spin the plate briefly and keep it at 4 °C until analysis.

### Additional Notes
The same steps are also available as an Opentrons Flex protocol (API 2.24, with liquid classes and liquid presence detection), generated from the same video: https://pugarhuda--show-dont-code-web.us-east.modal.run/api/runs/pcr_1-gt/protocol.py

###### Internal
sdc-pcr-setup-from-video

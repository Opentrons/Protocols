# Enzymatic Assay

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
	* Assay

## Description
This protocol performs a custom enzymatic assay on a temperature module-mounted deepwell plate and a temperature module-mounted PCR plate. Substrates 1-8 are transferred in order to column 1 of the deepwell plate, and substrates 9-16 are transferred in order to column 2 of the deepwell plate. The user is prompted to note times throughout the protocol.

For further instructions on setting up your 2 temperature modules for simultaneous use, please see 'Additional Notes' below. Note that during setup, temperature module 1 will be set to 37C (for the deepwell plate), and temperature module 2 will be set to 4C (for the PCR plate).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Eppendorf TwinTec 96-well PCR plate, skirted 150ul #951020406](https://online-shop.eppendorf.us/US-en/Laboratory-Consumables-44512/Plates-44516/Eppendorf-twin.tec-PCR-Plates-PF-8180.html)
* [Beckman Coulter 96-deepwell titer polypropylene plate 2ml #267006](https://www.beckman.com/supplies/plates/267004)
* [Opentrons 4x6 Eppendorf tuberack 1.5ml](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Opentrons temperature module with 96-well aluminum block x2](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [P50 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P300 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [Opentrons 300ul tip racks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 2)  
* channel 1: buffer
* channel 2: quenching solution

4x6 1.5ml Eppendorf tuberack (slot 5)  
* tubes A1-D4: substrates (substrate 1 in A1, substrate 2 in B1, ..., substrate 5 in A2, etc.)
* tube A5: enzyme

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P50 multi- and P300 single-channel pipette.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
Instructions for setting up your 2 temperature modules:
1. Plug in Module 1 to a power source, power it on and connect the USB cable to a port on your robot.
2. SSH into your robot:  
	* If you are using MacOS, open terminal and run ssh root@ROBOT_IP (replace ROBOT_IP with your robot's IP).
	* If you are using Windows:  
		* Download putty installer from [this link](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
		* Install and then open Putty
		* Under "Host Name (or IP address)", enter IP address found under "Connectivity" in "Robot" tab of the app. Note: do not enter a slash or numbers following a slash.
		* Ensure "Port" is 22 and "Connection type" is SSH
		* Click "Open" at the bottom
		* When terminal window pops up asking who to log in as, type in root and press enter
		* [Putty settings](https://www.dropbox.com/s/87bucxl2wqmo2is/Screenshot%202018-06-25%2013.57.19.png?dl=0)
	* Once you see the Opentrons logo, you have successfully SSH’d into the robot.
3. Find the device path of Module 1 by running `ls /dev/ttyACM*`
4. Use the device path in your protocol line 27.
5. Unplug Module 1, and plug in Module 2.
6. Repeat steps 3-4 to find the device path and replace it in line 10.
7. You can now safely exit the Terminal or Command Prompt.
8. Plug in Module 1 again, and you should now be able to control the Modules independently with your protocol.

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5001b8

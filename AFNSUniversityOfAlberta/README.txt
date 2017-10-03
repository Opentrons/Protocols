README

In a code text editor, such as Sublime Text (https://www.sublimetext.com/3), open the .py file for your protocol. 

Near the top of the file, locate the variable(s):

#volume master mix1
vol1 = 8 #can change here

#volume master mix2
vol2 = 8 #can change here

#volume cDNA
cdna_vol = 2 #can change here

#number of PCR strips you are using
num_strips = 6 #can change here, will change the below too 


#tubes with master mix in rack
master_mix1 = master_mixes.wells('A1') #can change position of master mix tubes here
master_mix2 = master_mixes.wells('A2') #can change position

 and change the variable(s) to the desired value(s) where there is some variation of "#change here", making sure to follow any specific directions if applicable.

Once you have changed all the necessary values, save the file and you will be ready to run your protocol per Opentrons' instructions.


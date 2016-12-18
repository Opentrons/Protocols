"""
Liquid Control

Demonstrates the usage for liquid-handling specific commands
"""

from opentrons import containers, instruments

plate = containers.load('96-flat', 'B1')

# to move liquide, first create a pipette with a maximum volume
pipette = instruments.Pipette(axis='b', max_volume=200)

pipette.aspirate(50, plate['A1'])  # aspirate 50uL from plate:A1
pipette.aspirate(50)               # aspirate 50uL from current position
pipette.aspirate(plate['A2'])      # aspirate until pipette fills from plate:A2

pipette.dispense(50, plate['B1'])  # dispense 50uL to plate:B1
pipette.dispense(50)               # dispense 50uL to current position
pipette.dispense(plate['B2'])      # dispense until pipette empties to plate:B2

pipette.blow_out()                 # blow out over current location
pipette.blow_out(plate['B3'])      # blow out over current plate:B3

pipette.touch_tip()                # touch tip within current location
pipette.touch_tip(plate['B1'])     # touch tip within plate:B1

pipette.mix(4, 100, plate['A2'])   # mix 4 times, 100uL, in plate:A2
pipette.mix(3, 50)                 # mix 3 times, 50uL, in current location
pipette.mix(2)                     # mix 2 times, pipette's full range, in current location

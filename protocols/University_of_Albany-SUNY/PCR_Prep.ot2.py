from opentrons import instruments, labware, modules

# labware setup
temp_deck = modules.load('tempdeck', '1')
plate_96 = labware.load('96-PCR-flat', '1', share=True)
plate_384 = labware.load('384-plate', '2')
tuberack = labware.load('tube-rack-2ml', '3')
source_tubes = tuberack.wells(0, length=8)

tiprack_10ul = labware.load('tiprack-10ul', '5')
tiprack_300ul = labware.load('opentrons-tiprack-300ul', '4')
tiprack2_300ul = labware.load('opentrons-tiprack-300ul', '6')
tiprack3_300ul = labware.load('opentrons-tiprack-300ul', '7')

# pipette setup
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_10ul]
    )

p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_300ul, tiprack2_300ul, tiprack3_300ul]
    )

# transfer PCR strip #1 to rows A, C, E, G, I, K, M, O
# transfer PCR strip #2 to rows B, D, F, H, J, L, N, P
m10.transfer(3, plate_96.cols('1'), [well for well in plate_384.rows('A')])
m10.transfer(3, plate_96.cols('2'), [well for well in plate_384.rows('B')])


# each source tube is distributed to 3 different columns in the plate
# distribute 7 uL to 6 wells every time it aspirates from the source
for index, each_tube in enumerate(source_tubes):
    p50.pick_up_tip()
    for row in plate_384.rows():
        for well in row.wells(index*3, length=3):
            # aspirate 42 uL every time the pipette volume is zero
            if p50.current_volume == 0:
                p50.aspirate(42, each_tube)

            # dispense at well edge
            p50.dispense(7, (well, well.from_center(x=1, y=0, z=0)))
    # changes tips between tips
    p50.drop_tip()

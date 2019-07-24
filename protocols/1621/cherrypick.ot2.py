from opentrons import labware, instruments, modules
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'Protein Normalization Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
source_name = 'Micronic-96-1-rack'
if source_name not in labware.list():
    labware.create(
        source_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=17,
        volume=50
    )

# load labware
step_dilution_plate = labware.load(
    'usascientific_96_wellplate_2.4ml_deep',
    '2',
    'step dilution plate'
)
source_rack = labware.load(source_name, '4', 'source rack')
buffer = labware.load('agilent_1_reservoir_290ml', '5', 'buffer').wells(0)
tips10 = labware.load('opentrons_96_tiprack_10ul', '7')
tips1000 = labware.load('opentrons_96_tiprack_1000ul', '8')

example_csv = """Protein Name,Well position,Protein Stock Concentration (µM),\
Desired concetration (µM),Total dilution factor,Step-dilution required,Step \
dilution factor,Final step dilution factor,Final volume of diluted protein \
required (µL)
MMP-A,A1,15,0.001,15000,yes,150,100,1000
MMP-B,B1,16.1,0.001,16100,yes,161,100,1000
MMP-C,C1,17.8,0.001,17800,yes,178,100,1000
MMP-D,D1,19.4,0.001,19400,yes,194,100,1000
MMP-E,E1,22.2,0.001,22200,yes,222,100,1000
MMP-F,F1,11.7,0.001,11700,yes,117,100,1000
MMP-G,G1,10.9,0.001,10900,yes,109,100,1000
MMP-H,H1,5.2,0.001,5200,yes,52,100,1000
MMP-I,A2,17.8,0.001,17800,yes,178,100,1000
MMP-J,B2,18.1,0.001,18100,yes,181,100,1000
MMP-K,C2,9.4,0.01,940,No,Not needed,Not needed,1000
MMP-L,D2,6.7,0.001,6700,yes,67,100,1000
MMP-M,E2,16.1,0.001,16100,yes,161,100,1000
MMP-N,F2,15.8,0.001,15800,yes,158,100,1000
MMP-O,G2,15.9,0.001,15900,yes,159,100,1000
"""


def run_custom_protocol(
        CSV_file: FileInput = example_csv,
        p10_mount: StringSelection('left', 'right') = 'left',
        p1000_mount: StringSelection('right', 'left') = 'right',
        temperature_module_temperature_in_degrees_C: float = 4
):
    # tempdeck setup
    tempdeck = modules.load('tempdeck', '1')
    dest_block = labware.load(
        'usascientific_96_wellplate_2.4ml_deep',
        '1',
        share=True
    )
    tempdeck.set_temperature(temperature_module_temperature_in_degrees_C)
    tempdeck.wait_for_temp()

    # pipettes
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=[tips10])
    p1000 = instruments.P1000_Single(mount=p1000_mount, tip_racks=[tips1000])

    # parse CSV
    data = [line.split(',') for line in CSV_file.splitlines()[1:] if line]

    for d in data:
        well_name = d[1].strip()
        step_dil = d[5].strip()
        source = source_rack.wells(well_name)
        final = dest_block.wells(well_name)

        if step_dil == 'yes':
            dil_x1 = float(d[6].strip())
            dil_x2 = float(d[7].strip())
            vol_p_1 = 1000/dil_x1
            vol_p_2 = 1000/dil_x2
            vol_buff_1 = 1000 - vol_p_1
            vol_buff_2 = 1000 - vol_p_2
            step = step_dilution_plate.wells(well_name)

            p1000.transfer(
                [vol_buff_1, vol_buff_2],
                buffer,
                [step.top(),
                 final.top()],
                blow_out=True
            )
            p10.pick_up_tip()
            p10.transfer(
                vol_p_1,
                source,
                step.bottom(),
                new_tip='never'
            )
            p10.mix(10, 9, step)
            p10.blow_out(step.top())
            p10.transfer(
                vol_p_2,
                step,
                final,
                new_tip='never'
            )
            p10.mix(10, 9, final)
            p10.blow_out(final.top())
            p10.drop_tip()
        else:
            dil_x = float(d[4].strip())
            vol_p = 1000/dil_x
            vol_buff = 1000 - vol_p

            p1000.transfer(
                vol_buff,
                buffer,
                final,
                blow_out=True
            )
            p10.pick_up_tip()
            p10.transfer(
                vol_p,
                source,
                final,
                new_tip='never'
            )
            p10.mix(10, 9, final)
            p10.blow_out(final.top())
            p10.drop_tip()

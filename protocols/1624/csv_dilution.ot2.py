from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'CSV Sample Dilution',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
custom_tips_name = 'custom-tips-300ul'
if custom_tips_name not in labware.list():
    labware.create(
        custom_tips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3,
        depth=60
        )

deepwell_name = 'Greiner-Masterblock-2ml'
if deepwell_name not in labware.list():
    labware.create(
        deepwell_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=40,
        volume=2000
    )

dil_plate_name = 'Nunc-96-well'
if dil_plate_name not in labware.list():
    labware.create(
        dil_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.7,
        depth=9.8,
        volume=450
    )

res_name = 'Agilent-1-well-reservoir'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=39.22,
        volume=290000
    )

# load labware
source_plate = labware.load(deepwell_name, '1', 'source plate')
dil_plates = [labware.load(
                  dil_plate_name,
                  slot,
                  'intermediate dilution plate ' + str(i+1)
              ) for i, slot in enumerate(['4', '5', '2'])]
end_plate = labware.load(dil_plate_name, '3', 'end plate')
h2o_res = labware.load(res_name, '6', 'H2O reservoir')
hcl_res = labware.load(res_name, '7', 'HCl reservoir')
tips = [labware.load(custom_tips_name, slot) for slot in ['8', '9']]

# reagents
h2o = h2o_res.wells('A1')
hcl = hcl_res.wells('A1')

# tip setup
h2o_tip = tips[0].wells('H12')

example_csv = """20,400,Empty,20,20,20,20,20,20,20,20,20,20
20,400,Empty,100,20,100,100,100,20,20,20,Empty,Empty,
20,400,Empty,100,20,100,100,100,20,20,20,Empty,Empty,
20,400,Empty,400,20,400,400,400,20,20,20,400,400
20,200,Empty,400,20,400,400,400,20,20,20,400,400
20,400,Empty,Empty,20,Empty,Empty,Empty,20,20,20,200,200
20,200,Empty,Empty,20,Empty,Empty,Empty,20,20,20,200,200
20,200,Empty,Empty,20,Empty,Empty,Empty,20,20,20,200,200
"""


def run_custom_protocol(
        csv_file: FileInput = example_csv,
        pipette_mount: StringSelection('right', 'left') = 'right',
        dilution_total_mixing_volume_in_ul: float = 300
):

    # volume check
    if (
            dilution_total_mixing_volume_in_ul > 300 or
            dilution_total_mixing_volume_in_ul < 30
    ):
        raise Exception('Invalid dilution total mixing volume.')

    # pipettes
    p300 = instruments.P300_Single(mount=pipette_mount, tip_racks=tips)

    # parse CSV
    dil_lines = csv_file.splitlines()[:8]
    dil_info = [dil.strip() for line in dil_lines
                for dil in line.split(',')[:12]]
    all_plates = [source_plate] + dil_plates + [end_plate]

    def dilution(dil_type, well_name):
        # set up proper dilution
        if dil_type == '20':
            num_dil_plates = 2
            h2o_vols = [dilution_total_mixing_volume_in_ul*0.9,
                        dilution_total_mixing_volume_in_ul*0.5]
        elif dil_type == '100':
            num_dil_plates = 2
            h2o_vols = [dilution_total_mixing_volume_in_ul*0.9,
                        dilution_total_mixing_volume_in_ul*0.9]
        elif dil_type == '200':
            num_dil_plates = 3
            h2o_vols = [dilution_total_mixing_volume_in_ul*0.9,
                        dilution_total_mixing_volume_in_ul*0.5,
                        dilution_total_mixing_volume_in_ul*0.9]
        elif dil_type == '400':
            num_dil_plates = 3
            h2o_vols = [dilution_total_mixing_volume_in_ul*0.9,
                        dilution_total_mixing_volume_in_ul*0.75,
                        dilution_total_mixing_volume_in_ul*0.9]
        dil_vols = [dilution_total_mixing_volume_in_ul-v for v in h2o_vols]

        p300.pick_up_tip()
        sources = [plate[well_name] for plate in all_plates[0:num_dil_plates]]
        dests = [plate[well_name] for plate in all_plates[1:num_dil_plates+1]]

        # add proper volume of H2O diluent to each dilution plate
        for vol, d in zip(h2o_vols, dests):
            p300.transfer(
                vol,
                h2o,
                d.top(),
                new_tip='never',
                blow_out=True
            )

        # perform dilutions across plates
        for vol, s, d in zip(dil_vols, sources, dests):
            p300.transfer(
                vol,
                s,
                d,
                new_tip='never'
            )
            p300.mix(5, 200, d)
            p300.blow_out(d.top())

        # transfer final dilution to end plate for 1:10 dilution in 0.1M HCl
        end = end_plate.wells(well_name)
        p300.transfer(
            30,
            dests[-1],
            end.top(),
            new_tip='never'
        )
        p300.drop_tip()

    # perform specified dilution
    all_source_wells = [well for row in source_plate.rows() for well in row]
    for source, dil_factor in zip(all_source_wells, dil_info):
        if dil_factor.strip() in ['20', '100', '200', '400']:
            well_name = source.get_name()
            dilution(dil_factor, well_name)

            # perform final 10x dilution in 0.1M HCl and mix
            end = end_plate.wells(well_name)
            p300.pick_up_tip()
            p300.transfer(
                dilution_total_mixing_volume_in_ul*0.9,
                hcl,
                end,
                new_tip='never'
            )
            p300.mix(5, 200, end)
            p300.drop_tip()

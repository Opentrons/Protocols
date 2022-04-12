"""PROTOCOL."""
import math
metadata = {
    'protocolName': 'Nucleic Acid Purification/Cloning',
    'author': 'Opentrons',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx):
    """PROTOCOL BODY."""
    [num_samples, omni_tray, heat_shock, agar_volume, dwp, dwp_volume
     ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples", "omni_tray", "heat_shock", "agar_volume",
        "dwp", "dwp_volume")

    # number of samples
    num_cols = math.ceil(num_samples/8)

    # load modules
    temp_1 = ctx.load_module('tempdeck', '1')
    temp_3 = ctx.load_module('tempdeck', '3')

    # load labware
    mix_n_go = temp_1.load_labware('azentalifesciences_96_wellplate_200ul')
    assemb_plate = temp_3.load_labware('azentalifesciences_96_wellplate_200ul')
    dwp_plate = ctx.load_labware('greiner_96_wellplate_2000ul', "11")

    dwp_dest_list = dwp_plate.rows()[0][:num_cols]
    samples_source_s = mix_n_go.wells()[:num_samples]
    samples_source_m = mix_n_go.rows()[0][:num_cols]
    assemb_liquid_m = assemb_plate.rows()[0][:num_cols]

    # load tipracks
    tiprack = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '4')]

    # load instrument
    p20 = ctx.load_instrument(
                        'p20_single_gen2',
                        mount='left',
                        tip_racks=tiprack
    )
    m20 = ctx.load_instrument(
                        'p20_multi_gen2',
                        mount='right',
                        tip_racks=tiprack
    )
    if omni_tray == '24':
        distro_source = samples_source_s
        agar_plates = [ctx.load_labware('customagar_24_wellplate_200ul', slot)
                       for slot in ['5', '6', '7', '8']]
        agar_pipette = p20
        agar_locations = [well for plate in agar_plates
                          for well in plate.wells()[:num_samples]]
        tip_recycle = tiprack[0].wells()[0:num_samples]
    else:
        distro_source = samples_source_m
        agar_plates = [ctx.load_labware('customagar_96_wellplate_200ul', slot)
                       for slot in ['9']]

        agar_pipette = m20
        agar_locations = [well for plate in agar_plates
                          for well in plate.rows()[0][:num_cols]]
        tip_recycle = tiprack[0].rows()[0][0:num_cols]

    # protocol
    temp_1.set_temperature(4)
    for source, dests in zip(assemb_liquid_m, samples_source_m):
        m20.transfer(5,
                     source,
                     dests,
                     new_tip='always',
                     mix_after=(3, 5),
                     blow_out=True,
                     blowout_location='destination well',
                     trash=False)

    # temp module to 42 celsius for 40s then back to 4 celsisus
    if heat_shock:
        temp_1.set_temperature(42)
        ctx.delay(seconds=40)
        temp_1.set_temperature(4)

    ctx.delay(minutes=30)

    # Agar Plate transfer
    for tips, source, dest in zip(tip_recycle, distro_source, agar_locations):
        agar_pipette.pick_up_tip(tips)
        agar_pipette.aspirate(agar_volume, source)
        agar_pipette.dispense(agar_volume, dest.top(5))
        agar_pipette.return_tip()

    # DWP/LC Addition If Needed
    if dwp:
        for tips, source, dest in zip(tip_recycle, samples_source_m,
                                      dwp_dest_list):
            m20.pick_up_tip(tips)
            m20.aspirate(dwp_volume, source)
            m20.dispense(dwp_volume, dest)
            m20.mix(10, 20, dest)
            m20.blow_out(dest.top(-1))
            m20.drop_tip()

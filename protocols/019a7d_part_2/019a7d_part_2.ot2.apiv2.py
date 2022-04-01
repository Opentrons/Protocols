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

    # define all custom variables above here with descriptions:

    # number of samples
    num_cols = math.ceil(num_samples/8)
    # "True" for park tips, "False" for discard tips

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
        tip_recycle = tiprack.wells()[:num_samples]
    else:
        distro_source = samples_source_m
        agar_plates = [ctx.load_labware('customagar_96_wellplate_200ul', slot)
                       for slot in ['9']]
        agar_pipette = m20
        agar_locations = [well for plate in agar_plates
                          for row in plate.rows()[0][:num_cols]
                          for well in row]
        tip_recycle = tiprack.rows()[:num_cols]

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
    """NEED 5MM ABOVE AGAR STILL!"""
    for source, dests in zip(distro_source, agar_locations):
        """agar_pipette.pick_up_tip()
        agar_pipette.aspirate(agar_volume, source)
        agar_pipette.dispense(agar_volume, dests.top(5))
        agar_pipette.return_tip()"""
        agar_pipette.transfer(agar_volume,
                              source,
                              dests,
                              trash=False
                              )
    # DWP/LC Addition If Needed
    if dwp:
        for source, dests in zip(samples_source_m, dwp_dest_list):
            m20.transfer(dwp_volume,
                         source,
                         dests,
                         new_tip='always'
                         )
    for c in ctx.commands():
        print(c)

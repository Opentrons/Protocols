import math

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
    }


def get_values(*names):
    import json
    _all_values = json.loads("""{ "number_of_samples":"80",
                                  "left_pipette":"p1000_single_gen2",
                                  "right_pipette":"p300_single_gen2",
                                  "mastermix_volume":"18",
                                  "DNA_volume":"2",
                                  "DNA_well_plate":"biorad_96_wellplate_200ul_pcr",
                                  "destination_well_plate":"biorad_96_wellplate_200ul_pcr"}
                                  """)
    return [_all_values[n] for n in names]


def run(protocol_context):
    [number_of_samples, left_pipette, right_pipette, mastermix_volume,
     DNA_volume, DNA_well_plate, destination_well_plate] \
      = get_values(  # noqa: F821
        "number_of_samples", "left_pipette", 'right_pipette',
        "mastermix_volume", "DNA_volume",
        "DNA_well_plate", "destination_well_plate"
     )

    number_of_samples = int(number_of_samples)
    mastermix_volume = int(mastermix_volume)
    DNA_volume = int(DNA_volume)

    # TODO: There should be a check here that the selected pipettes can
    # handle the DNA_volume and the mastermix_volume

    if not left_pipette and not right_pipette:
        raise Exception('You have to select at least 1 pipette.')

    pipette_l = None
    pipette_r = None

    for pip, mount, slots in zip(
            [left_pipette, right_pipette],
            ['left', 'right'],
            [['5', '6'], ['7', '8']]):

        if pip:
            range = pip.split('_')[0][1:]
            rack = 'opentrons_96_tiprack_' + range + 'ul'
            tipracks = [
                protocol_context.load_labware(rack, slot) for slot in slots]
            if mount == 'left':
                pipette_l = protocol_context.load_instrument(
                    pip, mount, tip_racks=tipracks)
            else:
                pipette_r = protocol_context.load_instrument(
                    pip, mount, tip_racks=tipracks)

    # labware setup
    dna_plate = protocol_context.load_labware(
        DNA_well_plate, '1', 'DNA plate')
    dest_plate = protocol_context.load_labware(
        destination_well_plate, '2', 'Output plate')
    res12 = protocol_context.load_labware(
        'usascientific_12_reservoir_22ml', '3', 'reservoir')

    # determine which pipette has the smaller volume range
    if pipette_l and pipette_r:
        if left_pipette == right_pipette:
            pip_s = pipette_l
            pip_l = pipette_r
        else:
            if pipette_l.max_volume < pipette_r.max_volume:
                pip_s, pip_l = pipette_l, pipette_r
            else:
                pip_s, pip_l = pipette_r, pipette_l
    else:
        pipette = pipette_l if pipette_l else pipette_r

    # reagent setup
    mastermix = res12.wells()[0]

    # The assumption here is that the samples will be a multiple of the
    # number of samples per column, which seems like a bad assumption
    """col_num = math.ceil(number_of_samples/8)

    # distribute mastermix
    # As the protocol is written it's assumed that the number of
    # samples are evenly divisible by the number of wells per column, i.e.
    # the samples
    if pipette_l and pipette_r:
        if mastermix_volume <= pip_s.max_volume:
            pipette = pip_s
        else:
            pipette = pip_l
    pipette.pick_up_tip()
    import pdb
    for dest in dest_plate.rows()[0][:col_num]:
        pdb.set_trace()
        pipette.transfer(
            mastermix_volume,
            mastermix,
            dest_plate.rows()[0][:col_num],
            new_tip='never'
        )
        pipette.blow_out(mastermix.top())
    pipette.drop_tip()"""

    # Make sure we have a pipette that can handle the volume of mastermix
    # Ideally the smaller one
    if pipette_l and pipette_r:
        """if mastermix_volume <= pip_s.max_volume:
            pipette = pip_s
        else:
            pipette = pip_l"""
        pipette = pipette_selector(pip_s, pip_l, mastermix_volume)
    pipette.pick_up_tip()

    # Let's assume that the samples are in column order so that we will go down
    # the columns first when we distribute the master mix.
    import pdb
    protocol_context.comment("Transferring master mix")
    dest_wells = dest_plate.wells()[:number_of_samples]
    # pdb.set_trace()
    for well in dest_wells:
        pipette.transfer(
            mastermix_volume,
            mastermix,
            well,
            new_tip='never'
        )
        # pipette.blow_out(mastermix.top())
    pipette.drop_tip()

    """# Transfer DNA
    if pipette_l and pipette_r:
        if DNA_volume <= pip_s.max_volume:
            pipette = pip_s
        else:
            pipette = pip_l
    for source, dest in zip(dna_plate.rows()[0][:col_num],
                            dest_plate.rows()[0][:col_num]):
        pipette.transfer(DNA_volume, source, dest)"""

    # Transfer DNA
    if pipette_l and pipette_r:
        pipette = pipette_selector(pip_s, pip_l, DNA_volume)

    protocol_context.comment("Transferring DNA")
    for source, dest in zip(dna_plate.wells()[:number_of_samples],
                            dest_plate.wells()[:number_of_samples]):
        pipette.transfer(DNA_volume, source, dest)

def pipette_selector(small_pipette, large_pipette, volume):
    if small_pipette and large_pipette:
        if volume <= small_pipette.max_volume:
            return small_pipette
        elif volume <= right_pipette.max_volume:
            return large_pipette
        else:
            raise Exception("There is no suitable pipette for this a volume of \
             {} uL".format(volume))

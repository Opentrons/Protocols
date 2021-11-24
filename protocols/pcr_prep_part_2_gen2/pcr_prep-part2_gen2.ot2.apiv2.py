import math

metadata = {
    'protocolName': 'PCR Prep part 2',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
    }


def run(protocol_context):
    [number_of_samples, left_pipette, right_pipette, mastermix_volume,
     DNA_volume, DNA_well_plate, destination_well_plate] \
      = get_values(  # noqa: F821
        "number_of_samples", "left_pipette", 'right_pipette',
        "mastermix_volume", "DNA_volume",
        "DNA_well_plate", "destination_well_plate"
     )

    number_of_samples = int(number_of_samples)
    mastermix_volume = float(mastermix_volume)
    DNA_volume = float(DNA_volume)

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
    pip_s, pip_l = rank_pipettes(pipette_l, pipette_r)

    # reagent setup
    mastermix = res12.wells()[0]

    # Make sure we have a pipette that can handle the volume of mastermix
    # Ideally the smaller one
    pipette = pipette_selector(pip_s, pip_l, mastermix_volume)

    col_num = math.ceil(number_of_samples/8)

    protocol_context.comment("Transferring master mix")
    pipette.pick_up_tip()
    for dest in dest_plate.rows()[0][:col_num]:
        pipette.transfer(
            mastermix_volume,
            mastermix,
            dest,
            new_tip='never'
        )
        pipette.blow_out(mastermix.top())
    pipette.drop_tip()

    # Transfer DNA to the destination plate
    pipette = pipette_selector(pip_s, pip_l, DNA_volume)

    protocol_context.comment("Transferring DNA")
    for source, dest in zip(dna_plate.rows()[0][:col_num],
                            dest_plate.rows()[0][:col_num]):
        pipette.transfer(DNA_volume, source, dest)


def rank_pipettes(pipette_l, pipette_r):
    """
    Given two pipettes this function will return them in the order of smallest
    to largest. This function assumes that error checking for cases where
    no pipettes were loaded was already done.
    """
    if not pipette_l:
        return [pipette_r, pipette_r]
    elif not pipette_r:
        return [pipette_l, pipette_l]
    else:
        if pipette_l.max_volume <= pipette_r.max_volume:
            return [pipette_l, pipette_r]
        else:
            return [pipette_r, pipette_l]


def pipette_selector(small_pipette, large_pipette, volume):
    """
    This function will return the smallest volume pipette capable
    of handling the given volume parameter.
    """
    if small_pipette and large_pipette:
        if (volume <= small_pipette.max_volume
           and volume <= small_pipette.min_volume):
            return small_pipette
        elif (volume <= large_pipette.max_volume
              and volume <= large_pipette.min_volume):
            return large_pipette
        else:
            raise Exception(("There is no suitable pipette loaded for "
                             "pipetting a volume of {} uL").format(volume))

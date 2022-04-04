from opentrons import protocol_api
from opentrons.protocol_api.labware import Well
from math import pi

metadata = {
    'protocolName': '022548-2 - DNA extraction',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def is_15ml_tube(well: Well):
    name = str(well).lower()
    if "tube" not in name or "15" not in name:
        return False
    return True


def tube_15ml_cone_height(tube: Well):
    """
    :return value: Approximate height of the tube cone
    """

    if not is_15ml_tube(tube):
        msg = ("The input well parameter: {}, does not appear to "
               "be a 15 mL tube")
        msg.format(tube)
        raise Exception(msg)
    return 0.171 * tube.depth


def tube_liq_height(vol, tube: Well, is_min_cone_height: bool = True):
    """
    Calculates the height of the liquid level in a conical tube
    given its liquid volume.The function tries to account for the conical
    part of the tube
    :param vol: The volume in uL
    :param tuberack: The tuberack with the tubes
    :param is_min_cone_height: Always return the height of the cone at
    minimum
    :return value: The height of the liquid level measured from
    the bottom in mm
    """

    if not is_15ml_tube(tube):
        msg = ("The input well parameter: {}, does not appear to "
               "be a 15 mL tube")
        msg.format(tube)
        raise Exception(msg)

    r = tube.diameter/2
    # Fudge factor - height seems too low given a volume, so bump it up
    # a little bit by "decreasing" the radius
    r *= 0.94

    # Cone height approximation
    h_cone_max = tube_15ml_cone_height(tube)
    vol_cone_max = (h_cone_max*pi*r**2)/3

    if vol < vol_cone_max:
        h_cone = (3*vol)/(pi*r**2)
        # print("h_cone", h_cone)
        if is_min_cone_height:
            return h_cone_max
        return h_cone
    else:
        cylinder_partial_vol = vol - vol_cone_max
        # print('cylinder v', cylinder_partial_vol,
        # 'cone max vol', vol_cone_max)
        h_partial_tube = cylinder_partial_vol/(pi*r**2)
        # print('h cone max', h_cone_max, 'h partial tube', h_partial_tube)
        return h_cone_max + h_partial_tube


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "n_tuberacks":3,
                                  "n_samples_rack_1":32,
                                  "n_samples_rack_2":32,
                                  "n_samples_rack_3":32,
                                  "master_mix_range":"1-3",
                                  "mastermix_max_vol":9.45,
                                  "mastermix_tuberack_lname":false,
                                  "mastermix_mix_rate_multiplier":0.3,
                                  "p300_mount":"left",
                                  "m300_mount":"right"
                                  }
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [n_tuberacks,
     n_samples_rack_1,
     n_samples_rack_2,
     n_samples_rack_3,
     master_mix_range,
     mastermix_max_vol,
     mastermix_tuberack_lname,
     mastermix_mix_rate_multiplier,
     p300_mount,
     m300_mount] = get_values(  # noqa: F821
     "n_tuberacks",
     "n_samples_rack_1",
     "n_samples_rack_2",
     "n_samples_rack_3",
     "master_mix_range",
     "mastermix_max_vol",
     "mastermix_tuberack_lname",
     "mastermix_mix_rate_multiplier",
     "p300_mount",
     "m300_mount")

    if n_tuberacks > 3 or n_tuberacks < 1:
        raise Exception(
            "The number of sample tube racks should be between 1 to 3 max")

    n_total_samples = 0
    for i, n in enumerate([n_samples_rack_1,
                           n_samples_rack_2,
                           n_samples_rack_3]):
        if n < 0 or n > 32:
            raise Exception(
                "Invalid number of samples (n={}) on tuberack #{}".format(
                    n, i+1)
                )
        n_total_samples += n

    # Define labware and slots
    sample_tuberack_loader = \
        ("nest_32_tuberack_8x15ml_8x15ml_8x15ml_8x15ml", ['2', '4', '7'])
    target_plate_loader = \
        ("thermofisherkingfisherdeepwell_96_wellplate_2000ul", '1')
    mastermix_source_lname = \
        ('nest_12_reservoir_15ml'
         if mastermix_tuberack_lname is False
         else mastermix_tuberack_lname)
    mastermix_labware_loader = (mastermix_source_lname, '10')
    sample_200ul_filtertiprack_loader = \
        ('opentrons_96_filtertiprack_200ul', '6')
    mastermix_300uL_tiprack_loader = ('opentrons_96_tiprack_300ul', '11')

    # define all custom variables above here with descriptions:

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''

    # load labware

    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''

    # load tipracks

    '''

    Add your tipracks here as a list:

    For a single tip rack:

    tiprack_name = [ctx.load_labware('{loadname}', '{slot number}')]

    For multiple tip racks of the same type:

    tiprack_name = [ctx.load_labware('{loadname}', 'slot')
                     for slot in ['1', '2', '3']]

    If two different tipracks are on the deck, use convention:
    tiprack[number of microliters]
    e.g. tiprack10, tiprack20, tiprack200, tiprack300, tiprack1000

    '''
    tiprack_200 = [ctx.load_labware(sample_200ul_filtertiprack_loader[0],
                                    sample_200ul_filtertiprack_loader[1])]
    tiprack_300 = [ctx.load_labware(mastermix_300uL_tiprack_loader[0],
                                    mastermix_300uL_tiprack_loader[1])]

    # load instrument

    '''
    Nomenclature for pipette:

    use 'p'  for single-channel, 'm' for multi-channel,
    followed by number of microliters.

    p20, p300, p1000 (single channel pipettes)
    m20, m300 (multi-channel pipettes)

    If loading pipette, load with:

    ctx.load_instrument(
                        '{pipette api load name}',
                        pipette_mount ("left", or "right"),
                        tip_racks=tiprack
                        )
    '''

    # pipette functions   # INCLUDE ANY BINDING TO CLASS

    '''

    Define all pipette functions, and class extensions here.
    These may include but are not limited to:

    - Custom pickup functions
    - Custom drop tip functions
    - Custom Tip tracking functions
    - Custom Trash tracking functions
    - Slow tip withdrawal

    For any functions in your protocol, describe the function as well as
    describe the parameters which are to be passed in as a docstring below
    the function (see below).

    def pick_up(pipette):
        """`pick_up()` will pause the protocol when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the protocol will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.

        :param pipette: The pipette desired to pick up tip
        as definited earlier in the protocol (e.g. p300, m20).
        """
        try:
            pipette.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            pipette.pick_up_tip()

    '''

    # helper functions
    '''
    Define any custom helper functions outside of the pipette scope here, using
    the convention seen above.

    e.g.

    def remove_supernatant(vol, index):
        """
        function description

        :param vol:

        :param index:
        """


    '''

    # reagents

    '''
    Define where all reagents are on the deck using the labware defined above.

    e.g.

    water = reservoir12.wells()[-1]
    waste = reservoir.wells()[0]
    samples = plate.rows()[0][0]
    dnase = tuberack.wells_by_name()['A4']

    '''

    # plate, tube rack maps

    '''
    Define any plate or tube maps here.

    e.g.

    plate_wells_by_row = [well for row in plate.rows() for well in row]

    '''

    # protocol

    '''

    Include header sections as follows for each "section" of your protocol.

    Section can be defined as a step in a bench protocol.

    e.g.

    ctx.comment('\n\nMOVING MASTERMIX TO SAMPLES IN COLUMNS 1-6\n')

    for .... in ...:
        ...
        ...

    ctx.comment('\n\nRUNNING THERMOCYCLER PROFILE\n')

    ...
    ...
    ...


    '''

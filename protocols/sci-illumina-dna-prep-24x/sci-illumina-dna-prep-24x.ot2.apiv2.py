from opentrons import protocol_api
from opentrons import types
import inspect

metadata = {
    'protocolName': 'Illumina DNA Prep 24x',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.9'
    }


def right(s, amount):
    if s is None:
        return None
    elif amount is None:
        return None  # Or throw a missing argument error
    s = str(s)
    if amount > len(s):
        return s
    elif amount == 0:
        return ""
    else:
        return s[-amount:]


def run(protocol: protocol_api.ProtocolContext):
    # labware
    mag_block = protocol.load_module('magnetic module gen2', '1')
    # Actually an Eppendorf 96 well, same dimensions
    sample_plate_mag =\
        mag_block.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    deepwell = protocol.load_labware('nest_96_wellplate_2ml_deep', '2')
    temp_block = protocol.load_module('temperature module gen2', '3')
    reagent_plate = temp_block.load_labware(
        'opentrons_96_aluminumblock_biorad_wellplate_200ul')
    tiprack_20 = protocol.load_labware('opentrons_96_filtertiprack_20ul',  '4')
    tiprack_200_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', '5')
    tiprack_200_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', '6')
    thermocycler = protocol.load_module('thermocycler module')
    sample_plate_thermo = thermocycler.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt')
    tiprack_200_3 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', '9')

    # reagent - plate
    Master_Tube_Tag = reagent_plate.wells_by_name()['A1']
    TSB = reagent_plate.wells_by_name()['A2']
    Master_Tube_PCR_1 = reagent_plate.wells_by_name()['A3']
    Barcodes1 = reagent_plate.wells_by_name()['A7']
    Barcodes2 = reagent_plate.wells_by_name()['A8']
    Barcodes3 = reagent_plate.wells_by_name()['A9']

    # reagent - eepwell
    AMPure = deepwell['A1']
    EtOH_1 = deepwell['A2']
    EtOH_2 = deepwell['A3']
    EtOH_3 = deepwell['A4']
    # RSB = deepwell['A6'] - unused
    TWB_1 = deepwell['A8']
    TWB_2 = deepwell['A9']
    TWB_3 = deepwell['A10']
    # Liquid_trash_2 = deepwell['A11'] - unused
    Liquid_trash_1 = deepwell['A12']

    # pipette
    p300 = protocol.load_instrument(
        'p300_multi_gen2', 'left',
        tip_racks=[tiprack_200_1, tiprack_200_2, tiprack_200_3])
    p20 = protocol.load_instrument(
        'p20_multi_gen2', 'right', tip_racks=[tiprack_20])

    # samples
    src_file_path = inspect.getfile(lambda: None)
    protocol.comment(src_file_path)
    if right(src_file_path, 5) == '8x.py':
        protocol.comment("There are 8 Samples")
        samplecolumns = 1
        TWB_washtip_1 = tiprack_200_1['A3']
        TWB_removetip_1 = tiprack_200_1['A4']
        ETOH_washtip_1 = tiprack_200_1['A9']
        ETOH_removetip_1 = tiprack_200_1['A10']
    elif right(src_file_path, 6) == '16x.py':
        protocol.comment("There are 16 Samples")
        samplecolumns = 2
        TWB_washtip_1 = tiprack_200_1['A5']
        TWB_washtip_2 = tiprack_200_1['A6']
        TWB_removetip_1 = tiprack_200_1['A7']
        TWB_removetip_2 = tiprack_200_1['A8']
        ETOH_washtip_1 = tiprack_200_2['A5']
        ETOH_washtip_2 = tiprack_200_2['A6']
        ETOH_removetip_1 = tiprack_200_2['A7']
        ETOH_removetip_2 = tiprack_200_2['A8']
    elif right(src_file_path, 6) == '24x.py':
        protocol.comment("There are 24 Samples")
        samplecolumns = 3
        TWB_washtip_1 = tiprack_200_1['A7']
        TWB_washtip_2 = tiprack_200_1['A8']
        TWB_washtip_3 = tiprack_200_1['A9']
        TWB_removetip_1 = tiprack_200_1['A10']
        TWB_removetip_2 = tiprack_200_1['A11']
        TWB_removetip_3 = tiprack_200_1['A12']
        ETOH_washtip_1 = tiprack_200_3['A7']
        ETOH_washtip_2 = tiprack_200_3['A8']
        ETOH_washtip_3 = tiprack_200_3['A9']
        ETOH_removetip_1 = tiprack_200_3['A10']
        ETOH_removetip_2 = tiprack_200_3['A11']
        ETOH_removetip_3 = tiprack_200_3['A12']
    else:
        protocol.pause("ERROR?")

    # offset
    p300_offset_Res = 2
    p300_offset_Thermo = 1
    p300_offset_Mag = 0.70
    p300_offset_Temp = 0.65

    p20_offset_Thermo = 1
    p20_offset_Mag = 0.75
    p20_offset_Temp = 0.85

    # positions
    ###########################################################################
    #  sample_plate_thermo on the Thermocycler
    A1_p20_bead_side = sample_plate_thermo['A1'].center().move(types.Point(
        x=-1.8*0.50, y=0, z=p20_offset_Thermo-5))  # Beads to the Right
    A1_p20_bead_top = sample_plate_thermo['A1'].center().move(types.Point(
        x=1.5, y=0, z=p20_offset_Thermo+2))  # Beads to the Right
    A1_p20_bead_mid = sample_plate_thermo['A1'].center().move(types.Point(
        x=1, y=0, z=p20_offset_Thermo-2))  # Beads to the Right
    A1_p300_bead_side = sample_plate_thermo['A1'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Thermo-7.2))  # Beads to the Right
    A1_p300_bead_top = sample_plate_thermo['A1'].center().move(types.Point(
        x=1.30, y=0, z=p300_offset_Thermo-1))  # Beads to the Right
    A1_p300_bead_mid = sample_plate_thermo['A1'].center().move(types.Point(
        x=0.80, y=0, z=p300_offset_Thermo-4))  # Beads to the Right
    A1_p300_loc1 = sample_plate_thermo['A1'].center().move(types.Point(
        x=1.3*0.8, y=1.3*0.8, z=p300_offset_Thermo-4))  # Beads to the Right
    A1_p300_loc2 = sample_plate_thermo['A1'].center().move(types.Point(
        x=1.3, y=0, z=p300_offset_Thermo-4))  # Beads to the Right
    A1_p300_loc3 = sample_plate_thermo['A1'].center().move(types.Point(
        x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Thermo-4))  # Beads to the Right
    A3_p20_bead_side = sample_plate_thermo['A3'].center().move(types.Point(
        x=-1.8*0.50, y=0, z=p20_offset_Thermo-5))  # Beads to the Right
    A3_p20_bead_top = sample_plate_thermo['A3'].center().move(types.Point(
        x=1.5, y=0, z=p20_offset_Thermo+2))  # Beads to the Right
    A3_p20_bead_mid = sample_plate_thermo['A3'].center().move(types.Point(
        x=1, y=0, z=p20_offset_Thermo-2))  # Beads to the Right
    A3_p300_bead_side = sample_plate_thermo['A3'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Thermo-7.2))  # Beads to the Right
    A3_p300_bead_top = sample_plate_thermo['A3'].center().move(types.Point(
        x=1.30, y=0, z=p300_offset_Thermo-1))  # Beads to the Right
    A3_p300_bead_mid = sample_plate_thermo['A3'].center().move(types.Point(
        x=0.80, y=0, z=p300_offset_Thermo-4))  # Beads to the Right
    A3_p300_loc1 = sample_plate_thermo['A3'].center().move(types.Point(
        x=1.3*0.8, y=1.3*0.8, z=p300_offset_Thermo-4))  # Beads to the Right
    A3_p300_loc2 = sample_plate_thermo['A3'].center().move(types.Point(
        x=1.3, y=0, z=p300_offset_Thermo-4))  # Beads to the Right
    A3_p300_loc3 = sample_plate_thermo['A3'].center().move(types.Point(
        x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Thermo-4))  # Beads to the Right
    A5_p20_bead_side = sample_plate_thermo['A5'].center().move(types.Point(
        x=-1.8*0.50, y=0, z=p20_offset_Thermo-5))  # Beads to the Right
    A5_p20_bead_top = sample_plate_thermo['A5'].center().move(types.Point(
        x=1.5, y=0, z=p20_offset_Thermo+2))  # Beads to the Right
    A5_p20_bead_mid = sample_plate_thermo['A5'].center().move(types.Point(
        x=1, y=0, z=p20_offset_Thermo-2))  # Beads to the Right
    A5_p300_bead_side = sample_plate_thermo['A5'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Thermo-7.2))  # Beads to the Right
    A5_p300_bead_top = sample_plate_thermo['A5'].center().move(types.Point(
        x=1.30, y=0, z=p300_offset_Thermo-1))  # Beads to the Right
    A5_p300_bead_mid = sample_plate_thermo['A5'].center().move(types.Point(
        x=0.80, y=0, z=p300_offset_Thermo-4))  # Beads to the Right
    A5_p300_loc1 = sample_plate_thermo['A5'].center().move(types.Point(
        x=1.3*0.8, y=1.3*0.8, z=p300_offset_Thermo-4))  # Beads to the Right
    A5_p300_loc2 = sample_plate_thermo['A5'].center().move(types.Point(
        x=1.3, y=0, z=p300_offset_Thermo-4))  # Beads to the Right
    A5_p300_loc3 = sample_plate_thermo['A5'].center().move(types.Point(
        x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Thermo-4))  # Beads to the Right
    ###########################################################################
    bypass = protocol.deck.position_for('11').move(
        types.Point(x=70, y=80, z=130))

    # commands
    protocol.comment("SETTING THERMO and TEMP BLOCK Temperature")
    thermocycler.set_block_temperature(4)
    thermocycler.set_lid_temperature(100)
    temp_block.set_temperature(4)

    thermocycler.open_lid()
    protocol.pause("Ready")

    protocol.comment('==============================================')
    protocol.comment('--> TAGMENTATION')
    protocol.comment('==============================================')

    protocol.comment('--> Adding Tagmentation Mix ')
    TagVol = 20
    TagMixRep = 10
    TagMixVol = 40
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A1'
        p300.pick_up_tip()
        p300.aspirate(TagVol, Master_Tube_Tag.bottom(
            z=p300_offset_Temp), rate=0.25)
        p300.dispense(TagVol, sample_plate_thermo[X].bottom(
            z=p300_offset_Thermo), rate=0.25)
        p300.move_to(sample_plate_thermo[X].bottom(z=p300_offset_Thermo))
        p300.mix(TagMixRep, TagMixVol)
        p300.blow_out(sample_plate_thermo[X].top(z=-5))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A3'
        p300.pick_up_tip()
        p300.aspirate(TagVol, Master_Tube_Tag.bottom(
            z=p300_offset_Temp), rate=0.25)
        p300.dispense(TagVol, sample_plate_thermo[X].bottom(
            z=p300_offset_Thermo), rate=0.25)
        p300.move_to(sample_plate_thermo[X].bottom(z=p300_offset_Thermo))
        p300.mix(TagMixRep, TagMixVol)
        p300.blow_out(sample_plate_thermo[X].top(z=-5))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A5'
        p300.pick_up_tip()
        p300.aspirate(TagVol, Master_Tube_Tag.bottom(
            z=p300_offset_Temp), rate=0.25)
        p300.dispense(TagVol, sample_plate_thermo[X].bottom(
            z=p300_offset_Thermo), rate=0.25)
        p300.move_to(sample_plate_thermo[X].bottom(z=p300_offset_Thermo))
        p300.mix(TagMixRep, TagMixVol)
        p300.blow_out(sample_plate_thermo[X].top(z=-5))
        p300.move_to(bypass)
        p300.drop_tip()

    ###########################################################################
    protocol.pause('Seal, Run TAG (15min)')

    thermocycler.close_lid()
    profile_TAG = [
        {'temperature': 55, 'hold_time_minutes': 15}
        ]
    thermocycler.execute_profile(
        steps=profile_TAG, repetitions=1, block_max_volume=50)
    thermocycler.set_block_temperature(10)
    ###########################################################################
    thermocycler.open_lid()
    protocol.pause("Remove Seal")

    protocol.comment('--> Adding Tagmentation Stop Buffer')
    TSBVol = 20
    TSBMixRep = 10
    TSBMixVol = 20
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A1'
        p20.pick_up_tip()
        p20.aspirate(TSBVol, TSB.bottom(z=p20_offset_Temp))
        p20.dispense(TSBVol, sample_plate_thermo[X].bottom(
            z=p20_offset_Thermo))
        p20.mix(TSBMixRep, TSBMixVol)
        p20.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A3'
        p20.pick_up_tip()
        p20.aspirate(TSBVol, TSB.bottom(z=p20_offset_Temp))
        p20.dispense(TSBVol, sample_plate_thermo[X].bottom(
            z=p20_offset_Thermo))
        p20.mix(TSBMixRep, TSBMixVol)
        p20.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A5'
        p20.pick_up_tip()
        p20.aspirate(TSBVol, TSB.bottom(z=p20_offset_Temp))
        p20.dispense(TSBVol, sample_plate_thermo[X].bottom(
            z=p20_offset_Thermo))
        p20.mix(TSBMixRep, TSBMixVol)
        p20.drop_tip()

    ###########################################################################
    protocol.pause('Seal, Run PTC (15min)')

    thermocycler.close_lid()
    profile_PTC = [
        {'temperature': 37, 'hold_time_minutes': 15}
        ]
    thermocycler.execute_profile(
        steps=profile_PTC, repetitions=1, block_max_volume=60)
    thermocycler.set_block_temperature(10)
    ###########################################################################
    thermocycler.open_lid()
    protocol.pause("Remove Seal")

    protocol.comment('==============================================')
    protocol.comment('--> TAGMENTATION WASH')
    protocol.comment('==============================================')

    protocol.pause("PLACE sample_plate on MAGNET")

    # positions
    # UNUSED VARIABLES COMMENTED OUT
    ###########################################################################
    #  sample_plate_mag on the Mag Block
    # A1_p20_bead_top, side and mid are unused variables
    # A1_p20_bead_side = sample_plate_mag['A1'].center().move(types.Point(
    #    x=-1.8*0.50, y=0, z=p20_offset_Mag-5)) #Beads to the Right
    # A1_p20_bead_top = sample_plate_mag['A1'].center().move(types.Point(
    #    x=1.5, y=0, z=p20_offset_Mag+2)) #Beads to the Right
    # A1_p20_bead_mid = sample_plate_mag['A1'].center().move(types.Point(
    #    x=1, y=0, z=p20_offset_Mag-2)) #Beads to the Right
    A1_p300_bead_side = sample_plate_mag['A1'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Mag-7.2))  # Beads to the Right
    A1_p300_bead_top = sample_plate_mag['A1'].center().move(types.Point(
        x=1.30, y=0, z=p300_offset_Mag-1))  # Beads to the Right
    A1_p300_bead_mid = sample_plate_mag['A1'].center().move(types.Point(
        x=0.80, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    A1_p300_loc1 = sample_plate_mag['A1'].center().move(types.Point(
        x=1.3*0.8, y=1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    A1_p300_loc2 = sample_plate_mag['A1'].center().move(types.Point(
        x=1.3, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    A1_p300_loc3 = sample_plate_mag['A1'].center().move(types.Point(
        x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A3_p20_bead_side = sample_plate_mag['A3'].center().move(types.Point(
    #    x=-1.8*0.50, y=0, z=p20_offset_Mag-5)) #Beads to the Right
    # A3_p20_bead_top = sample_plate_mag['A3'].center().move(types.Point(
    #    x=1.5, y=0, z=p20_offset_Mag+2)) #Beads to the Right
    # A3_p20_bead_mid = sample_plate_mag['A3'].center().move(types.Point(
    #    x=1, y=0, z=p20_offset_Mag-2)) #Beads to the Right
    A3_p300_bead_side = sample_plate_mag['A3'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Mag-7.2))  # Beads to the Right
    A3_p300_bead_top = sample_plate_mag['A3'].center().move(types.Point(
        x=1.30, y=0, z=p300_offset_Mag-1))  # Beads to the Right
    A3_p300_bead_mid = sample_plate_mag['A3'].center().move(types.Point(
        x=0.80, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    A3_p300_loc1 = sample_plate_mag['A3'].center().move(types.Point(
        x=1.3*0.8, y=1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    A3_p300_loc2 = sample_plate_mag['A3'].center().move(types.Point(
        x=1.3, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    A3_p300_loc3 = sample_plate_mag['A3'].center().move(types.Point(
        x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A5_p20_bead_side = sample_plate_mag['A5'].center().move(types.Point(
    #    x=-1.8*0.50, y=0, z=p20_offset_Mag-5))  # Beads to the Right
    # A5_p20_bead_top = sample_plate_mag['A5'].center().move(types.Point(
    #    x=1.5, y=0, z=p20_offset_Mag+2))  # Beads to the Right
    # A5_p20_bead_mid = sample_plate_mag['A5'].center().move(types.Point(
    #    x=1, y=0, z=p20_offset_Mag-2))  # Beads to the Right
    A5_p300_bead_side = sample_plate_mag['A5'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Mag-7.2))  # Beads to the Right
    A5_p300_bead_top = sample_plate_mag['A5'].center().move(types.Point(
        x=1.30, y=0, z=p300_offset_Mag-1))  # Beads to the Right
    A5_p300_bead_mid = sample_plate_mag['A5'].center().move(types.Point(
        x=0.80, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    A5_p300_loc1 = sample_plate_mag['A5'].center().move(types.Point(
        x=1.3*0.8, y=1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    A5_p300_loc2 = sample_plate_mag['A5'].center().move(types.Point(
        x=1.3, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    A5_p300_loc3 = sample_plate_mag['A5'].center().move(types.Point(
        x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A7_p20_bead_side = sample_plate_mag['A7'].center().move(types.Point(
    #    x=-1.8*0.50, y=0, z=p20_offset_Mag-5))  # Beads to the Right
    # A7_p20_bead_top = sample_plate_mag['A7'].center().move(types.Point(
    #    x=1.5, y=0, z=p20_offset_Mag+2))  # Beads to the Right
    # A7_p20_bead_mid = sample_plate_mag['A7'].center().move(types.Point(
    #    x=1, y=0, z=p20_offset_Mag-2))  # Beads to the Right
    A7_p300_bead_side = sample_plate_mag['A7'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Mag-7.2))  # Beads to the Right
    # A7_p300_bead_top = sample_plate_mag['A7'].center().move(types.Point(
    #    x=1.30, y=0, z=p300_offset_Mag-1))  # Beads to the Right
    # A7_p300_bead_mid = sample_plate_mag['A7'].center().move(types.Point(
    #    x=0.80, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    # A7_p300_loc1 = sample_plate_mag['A7'].center().move(types.Point(
    #    x=1.3*0.8, y=1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A7_p300_loc2 = sample_plate_mag['A7'].center().move(types.Point(
    #    x=1.3, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    # A7_p300_loc3 = sample_plate_mag['A7'].center().move(types.Point(
    #    x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A9_p20_bead_side = sample_plate_mag['A9'].center().move(types.Point(
    #    x=-1.8*0.50, y=0, z=p20_offset_Mag-5))  # Beads to the Right
    # A9_p20_bead_top = sample_plate_mag['A9'].center().move(types.Point(
    #    x=1.5, y=0, z=p20_offset_Mag+2))  # Beads to the Right
    #     A9_p20_bead_mid = sample_plate_mag['A9'].center().move(types.Point(
    #        x=1, y=0, z=p20_offset_Mag-2))  # Beads to the Right
    A9_p300_bead_side = sample_plate_mag['A9'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Mag-7.2))  # Beads to the Right
    # A9_p300_bead_top = sample_plate_mag['A9'].center().move(types.Point(
    #    x=1.30, y=0, z=p300_offset_Mag-1))  # Beads to the Right
    # A9_p300_bead_mid = sample_plate_mag['A9'].center().move(types.Point(
    #    x=0.80, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    # A9_p300_loc1 = sample_plate_mag['A9'].center().move(types.Point(
    #    x=1.3*0.8, y=1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A9_p300_loc2 = sample_plate_mag['A9'].center().move(types.Point(
    #    x=1.3, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    # A9_p300_loc3 = sample_plate_mag['A9'].center().move(types.Point(
    #    x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A11_p20_bead_side = sample_plate_mag['A11'].center().move(types.Point(
    #    x=-1.8*0.50, y=0, z=p20_offset_Mag-5))  # Beads to the Right
    # A11_p20_bead_top = sample_plate_mag['A11'].center().move(types.Point(
    #    x=1.5, y=0, z=p20_offset_Mag+2))  # Beads to the Right
    # A11_p20_bead_mid = sample_plate_mag['A11'].center().move(types.Point(
    #    x=1, y=0, z=p20_offset_Mag-2))  # Beads to the Right
    A11_p300_bead_side = sample_plate_mag['A11'].center().move(types.Point(
        x=-0.50, y=0, z=p300_offset_Mag-7.2))  # Beads to the Right
    # A11_p300_bead_top = sample_plate_mag['A11'].center().move(types.Point(
    #    x=1.30, y=0, z=p300_offset_Mag-1))  # Beads to the Right
    # A11_p300_bead_mid = sample_plate_mag['A11'].center().move(types.Point(
    #    x=0.80, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    # A11_p300_loc1 = sample_plate_mag['A11'].center().move(types.Point(
    #    x=1.3*0.8, y=1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    # A11_p300_loc2 = sample_plate_mag['A11'].center().move(types.Point(
    #    x=1.3, y=0, z=p300_offset_Mag-4))  # Beads to the Right
    # A11_p300_loc3 = sample_plate_mag['A11'].center().move(types.Point(
    #    x=1.3*0.8, y=-1.3*0.8, z=p300_offset_Mag-4))  # Beads to the Right
    ###########################################################################
    protocol.comment('MAGNET ENGAGE')
    mag_block.engage(height_from_base=17)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=14)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=10)
    protocol.delay(minutes=1)

    protocol.comment('--> Removing Supernatant')
    RemoveSup = 75
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A1'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(RemoveSup-20, rate=0.25)
        p300.default_speed = 5
        if X == 'A1':
            p300.move_to(A1_p300_bead_side)
        if X == 'A3':
            p300.move_to(A3_p300_bead_side)
        if X == 'A5':
            p300.move_to(A5_p300_bead_side)
        protocol.delay(minutes=0.1)
        p300.aspirate(20, rate=0.2)
        p300.move_to(sample_plate_mag[X].top(z=2))
        p300.default_speed = 400
        p300.dispense(200, Liquid_trash_1)
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A3'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(RemoveSup-20, rate=0.25)
        p300.default_speed = 5
        if X == 'A1':
            p300.move_to(A1_p300_bead_side)
        if X == 'A3':
            p300.move_to(A3_p300_bead_side)
        if X == 'A5':
            p300.move_to(A5_p300_bead_side)
        protocol.delay(minutes=0.1)
        p300.aspirate(20, rate=0.2)
        p300.move_to(sample_plate_mag[X].top(z=2))
        p300.default_speed = 400
        p300.dispense(200, Liquid_trash_1)
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A5'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(RemoveSup-20, rate=0.25)
        p300.default_speed = 5
        if X == 'A1': p300.move_to(A1_p300_bead_side)
        if X == 'A3': p300.move_to(A3_p300_bead_side)
        if X == 'A5': p300.move_to(A5_p300_bead_side)
        protocol.delay(minutes=0.1)
        p300.aspirate(20, rate=0.2)
        p300.move_to(sample_plate_mag[X].top(z=2))
        p300.default_speed = 400
        p300.dispense(200, Liquid_trash_1)
        p300.move_to(bypass)
        p300.drop_tip()

    protocol.comment('MAGNET DISENGAGE')
    mag_block.disengage()

    protocol.comment('--> Repeating 3 washes')
    washreps = 3
    for wash in range(washreps):
        protocol.comment('--> TWB Wash #'+str(wash+1))
        TWBMixRep = 15
        TWBMixVol = 70
        if samplecolumns >= 1:  # -------------------------------------------------
            X = 'A1'
            p300.pick_up_tip(TWB_washtip_1)
            p300.aspirate(100, TWB_1.bottom(z=p300_offset_Res))
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(100, rate=0.75)
            p300.default_speed = 5
            reps = 4
            for x in range(reps):
                p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
                p300.aspirate(100)
                if X == 'A1': p300.move_to(A1_p300_bead_top)
                if X == 'A3': p300.move_to(A3_p300_bead_top)
                if X == 'A5': p300.move_to(A5_p300_bead_top)
                p300.dispense(100, rate=0.75)
            if X == 'A1': p300.move_to(A1_p300_bead_mid)
            if X == 'A3': p300.move_to(A3_p300_bead_mid)
            if X == 'A5': p300.move_to(A5_p300_bead_mid)
            p300.mix(TWBMixRep, TWBMixVol)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.mix(TWBMixRep, TWBMixVol)
            p300.default_speed = 400
            p300.move_to(bypass)
            protocol.pause("TIP CHECK - once per wash")
            p300.return_tip()
        if samplecolumns >= 2:  # -------------------------------------------------
            X = 'A3'
            p300.pick_up_tip(TWB_washtip_2)
            p300.aspirate(100, TWB_2.bottom(z=p300_offset_Res))
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(100, rate=0.75)
            p300.default_speed = 5
            reps = 4
            for x in range(reps):
                p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
                p300.aspirate(100)
                if X == 'A1': p300.move_to(A1_p300_bead_top)
                if X == 'A3': p300.move_to(A3_p300_bead_top)
                if X == 'A5': p300.move_to(A5_p300_bead_top)
                p300.dispense(100, rate=0.75)
            if X == 'A1': p300.move_to(A1_p300_bead_mid)
            if X == 'A3': p300.move_to(A3_p300_bead_mid)
            if X == 'A5': p300.move_to(A5_p300_bead_mid)
            p300.mix(TWBMixRep, TWBMixVol)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.mix(TWBMixRep, TWBMixVol)
            p300.default_speed = 400
            p300.move_to(bypass)
            p300.return_tip()
        if samplecolumns >= 3:  # -------------------------------------------------
            X = 'A5'
            p300.pick_up_tip(TWB_washtip_3)
            p300.aspirate(100, TWB_3.bottom(z=p300_offset_Res))
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(100, rate=0.75)
            p300.default_speed = 5
            reps = 4
            for x in range(reps):
                p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
                p300.aspirate(100)
                if X == 'A1': p300.move_to(A1_p300_bead_top)
                if X == 'A3': p300.move_to(A3_p300_bead_top)
                if X == 'A5': p300.move_to(A5_p300_bead_top)
                p300.dispense(100, rate=0.75)
            if X == 'A1': p300.move_to(A1_p300_bead_mid)
            if X == 'A3': p300.move_to(A3_p300_bead_mid)
            if X == 'A5': p300.move_to(A5_p300_bead_mid)
            p300.mix(TWBMixRep, TWBMixVol)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.mix(TWBMixRep, TWBMixVol)
            p300.default_speed = 400
            p300.move_to(bypass)
            p300.return_tip()

        protocol.comment('MAGNET ENGAGE')
        mag_block.engage(height_from_base=17)
        protocol.delay(minutes=1)
        mag_block.engage(height_from_base=14)
        protocol.delay(minutes=1)
        mag_block.engage(height_from_base=10)
        protocol.delay(minutes=1)

        protocol.comment('--> Remove TWB Wash #'+str(wash+1))
        if samplecolumns >= 1:  # --------------------------------------------
            X = 'A1'
            p300.pick_up_tip(TWB_removetip_1)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
            p300.aspirate(75, rate=0.25)
            p300.default_speed = 5
            if X == 'A1': p300.move_to(A1_p300_bead_side)
            if X == 'A3': p300.move_to(A3_p300_bead_side)
            if X == 'A5': p300.move_to(A5_p300_bead_side)
            protocol.delay(minutes=0.1)
            p300.aspirate(20, rate=0.2)
            p300.move_to(sample_plate_mag[X].top(z=2))
            p300.default_speed = 400
            p300.dispense(200, Liquid_trash_1)
            p300.move_to(bypass)
            protocol.pause("TIP CHECK - once per wash")
            p300.return_tip()
        if samplecolumns >= 2:  # --------------------------------------------
            X = 'A3'
            p300.pick_up_tip(TWB_removetip_2)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
            p300.aspirate(75, rate=0.25)
            p300.default_speed = 5
            if X == 'A1':
                p300.move_to(A1_p300_bead_side)
            if X == 'A3':
                p300.move_to(A3_p300_bead_side)
            if X == 'A5':
                p300.move_to(A5_p300_bead_side)
            protocol.delay(minutes=0.1)
            p300.aspirate(20, rate=0.2)
            p300.move_to(sample_plate_mag[X].top(z=2))
            p300.default_speed = 400
            p300.dispense(200, Liquid_trash_1)
            p300.move_to(bypass)
            p300.return_tip()
        if samplecolumns >= 3:  # --------------------------------------------
            X = 'A5'
            p300.pick_up_tip(TWB_removetip_3)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
            p300.aspirate(75, rate=0.25)
            p300.default_speed = 5
            if X == 'A1': p300.move_to(A1_p300_bead_side)
            if X == 'A3': p300.move_to(A3_p300_bead_side)
            if X == 'A5': p300.move_to(A5_p300_bead_side)
            protocol.delay(minutes=0.1)
            p300.aspirate(20, rate=0.2)
            p300.move_to(sample_plate_mag[X].top(z=2))
            p300.default_speed = 400
            p300.dispense(200, Liquid_trash_1)
            p300.move_to(bypass)
            p300.return_tip()

        protocol.comment('MAGNET DISENGAGE')
        mag_block.disengage()
        wash += 1

    protocol.comment('MAGNET ENGAGE')
    mag_block.engage(height_from_base=10)

    protocol.comment('==============================================')
    protocol.comment('--> AMPLIFICATION')
    protocol.comment('==============================================')

    protocol.comment('--> Removing Residual Supernatant')
    if samplecolumns >= 1:  # ------------------------------------------------
        X = 'A1'
        p20.pick_up_tip()
        p20.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p20.aspirate(20, rate=0.25)
        p20.move_to(bypass)
        p20.drop_tip()
    if samplecolumns >= 2:  # ------------------------------------------------
        X = 'A3'
        p20.pick_up_tip()
        p20.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p20.aspirate(20, rate=0.25)
        p20.move_to(bypass)
        p20.drop_tip()
    if samplecolumns >= 3:  # ------------------------------------------------
        X = 'A5'
        p20.pick_up_tip()
        p20.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p20.aspirate(20, rate=0.25)
        p20.move_to(bypass)
        p20.drop_tip()

    mag_block.engage(height_from_base=6)
    protocol.delay(minutes=0.5)

    protocol.comment('MAGNET DISENGAGE')
    mag_block.disengage()

    protocol.comment('ADDING Master_Tube_PCR')
    PCRVol = 40
    PCRMixRep = 5
    PCRMixVol = 30
    if samplecolumns >= 1:  # ------------------------------------------------
        X = 'A1'
        p300.pick_up_tip()
        p300.aspirate(PCRVol, Master_Tube_PCR_1.bottom(p300_offset_Temp))
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        p300.default_speed = 5
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc3)
        if X == 'A3': p300.move_to(A3_p300_loc3)
        if X == 'A5': p300.move_to(A5_p300_loc3)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        reps = 5
        for x in range(reps):
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(PCRVol, rate=0.5)
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(PCRVol, rate=1)
        reps = 3
        for x in range(reps):
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc1)
            if X == 'A3': p300.move_to(A3_p300_loc1)
            if X == 'A5': p300.move_to(A5_p300_loc1)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc3)
            if X == 'A3': p300.move_to(A3_p300_loc3)
            if X == 'A5': p300.move_to(A5_p300_loc3)
            p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
        p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag[X].top())
        protocol.delay(seconds=0.5)
        p300.move_to(sample_plate_mag[X].center())
        p300.default_speed = 400
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A3'
        p300.pick_up_tip()
        p300.aspirate(PCRVol, Master_Tube_PCR_1.bottom(p300_offset_Temp))
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        p300.default_speed = 5
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc3)
        if X == 'A3': p300.move_to(A3_p300_loc3)
        if X == 'A5': p300.move_to(A5_p300_loc3)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        reps = 5
        for x in range(reps):
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(PCRVol, rate=0.5)
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(PCRVol, rate=1)
        reps = 3
        for x in range(reps):
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc1)
            if X == 'A3': p300.move_to(A3_p300_loc1)
            if X == 'A5': p300.move_to(A5_p300_loc1)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc3)
            if X == 'A3': p300.move_to(A3_p300_loc3)
            if X == 'A5': p300.move_to(A5_p300_loc3)
            p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
        p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag[X].top())
        protocol.delay(seconds=0.5)
        p300.move_to(sample_plate_mag[X].center())
        p300.default_speed = 400
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A5'
        p300.pick_up_tip()
        p300.aspirate(PCRVol, Master_Tube_PCR_1.bottom(p300_offset_Temp))
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        p300.default_speed = 5
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc3)
        if X == 'A3': p300.move_to(A3_p300_loc3)
        if X == 'A5': p300.move_to(A5_p300_loc3)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        reps = 5
        for x in range(reps):
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(PCRVol, rate=0.5)
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(PCRVol, rate=1)
        reps = 3
        for x in range(reps):
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc1)
            if X == 'A3': p300.move_to(A3_p300_loc1)
            if X == 'A5': p300.move_to(A5_p300_loc1)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc3)
            if X == 'A3': p300.move_to(A3_p300_loc3)
            if X == 'A5': p300.move_to(A5_p300_loc3)
            p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
        p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag[X].top())
        protocol.delay(seconds=0.5)
        p300.move_to(sample_plate_mag[X].center())
        p300.default_speed = 400
        p300.drop_tip()

    protocol.comment('--> Adding Barcodes')
    BarcodeVol    = 10
    BarcodeMixRep = 10
    BarcodeMixVol = 10
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A1'
        p20.pick_up_tip()
        p20.aspirate(BarcodeVol, Barcodes1)
        p20.dispense(BarcodeVol, sample_plate_mag[X].bottom(z=p20_offset_Mag))
        p20.mix(BarcodeMixRep, BarcodeMixVol)
        p20.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A3'
        p20.pick_up_tip()
        p20.aspirate(BarcodeVol, Barcodes2)
        p20.dispense(BarcodeVol, sample_plate_mag[X].bottom(z=p20_offset_Mag))
        p20.mix(BarcodeMixRep, BarcodeMixVol)
        p20.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A5'
        p20.pick_up_tip()
        p20.aspirate(BarcodeVol, Barcodes3)
        p20.dispense(BarcodeVol, sample_plate_mag[X].bottom(z=p20_offset_Mag))
        p20.mix(BarcodeMixRep, BarcodeMixVol)
        p20.drop_tip()

    protocol.pause("PLACE sample_plate on THERMO")

    ###########################################################################    protocol.pause('Seal, Run PCR (25min)')

    thermocycler.close_lid()
    profile_PCR_1 = [
        {'temperature': 68, 'hold_time_minutes': 3},
        {'temperature': 98, 'hold_time_minutes': 3}
        ]
    thermocycler.execute_profile(steps=profile_PCR_1, repetitions=1, block_max_volume=50)
    profile_PCR_2 = [
        {'temperature': 98, 'hold_time_seconds': 45},
        {'temperature': 62, 'hold_time_seconds': 30},
        {'temperature': 68, 'hold_time_minutes': 2}
        ]
    thermocycler.execute_profile(steps=profile_PCR_2, repetitions=5, block_max_volume=50)
    profile_PCR_3 = [
        {'temperature': 68, 'hold_time_minutes': 1}
        ]
    thermocycler.execute_profile(steps=profile_PCR_3, repetitions=1, block_max_volume=50)
    thermocycler.set_block_temperature(4)
    ###########################################################################
    thermocycler.open_lid()
    protocol.pause("Remove Seal")

    protocol.comment('==============================================')
    protocol.comment('--> CLEANUP')
    protocol.comment('==============================================')

    protocol.pause("PLACE sample_plate on MAGNET")

    protocol.comment('MAGNET ENGAGE')
    mag_block.engage(height_from_base=17)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=14)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=10)
    protocol.delay(minutes=1)

    protocol.comment('--> Transferring Supernatant')
    TransferSup = 45
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A1'
        Y = 'A7'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(TransferSup, rate=0.25)
        p300.dispense(TransferSup+5, sample_plate_mag[Y].bottom(z=p300_offset_Mag))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A3'
        Y = 'A9'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(TransferSup, rate=0.25)
        p300.dispense(TransferSup+5, sample_plate_mag[Y].bottom(z=p300_offset_Mag))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A5'
        Y = 'A11'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(TransferSup, rate=0.25)
        p300.dispense(TransferSup+5, sample_plate_mag[Y].bottom(z=p300_offset_Mag))
        p300.move_to(bypass)
        p300.drop_tip()

    protocol.comment('MAGNET DISENGAGE')
    mag_block.disengage()

    protocol.comment('--> ADDING AMPure')
    AMPureVol = 81
    AMPureMixRep = 50
    AMPureMixVol = 126
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A7'
        p300.pick_up_tip()
        p300.mix(10, AMPureVol+10, AMPure)
        p300.aspirate(81, AMPure, rate=0.25)
        p300.dispense(81, sample_plate_mag[X].bottom(z=p300_offset_Mag), rate=0.25)
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
        p300.mix(AMPureMixRep, AMPureMixVol)
        p300.blow_out(sample_plate_mag[X].top(z=-5))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A9'
        p300.pick_up_tip()
        p300.mix(3, AMPureVol+10, AMPure)
        p300.aspirate(81, AMPure, rate=0.25)
        p300.dispense(81, sample_plate_mag[X].bottom(z=p300_offset_Mag), rate=0.25)
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
        p300.mix(AMPureMixRep, AMPureMixVol)
        p300.blow_out(sample_plate_mag[X].top(z=-5))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A11'
        p300.pick_up_tip()
        p300.mix(3, AMPureVol+10, AMPure)
        p300.aspirate(81, AMPure, rate=0.25)
        p300.dispense(81, sample_plate_mag[X].bottom(z=p300_offset_Mag), rate=0.25)
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
        p300.mix(AMPureMixRep, AMPureMixVol)
        p300.blow_out(sample_plate_mag[X].top(z=-5))
        p300.move_to(bypass)
        p300.drop_tip()

    protocol.delay(minutes=5)

    protocol.comment('MAGNET ENGAGE')
    mag_block.engage(height_from_base=17)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=15)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=14)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=12)
    protocol.delay(minutes=1)
    mag_block.engage(height_from_base=10)
    protocol.delay(minutes=1)

    protocol.comment('--> Removing Supernatant')
    RemoveSup = 120
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A7'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(RemoveSup-20, rate=0.25)
        p300.default_speed = 5
        if X == 'A7': p300.move_to(A7_p300_bead_side)
        if X == 'A9': p300.move_to(A9_p300_bead_side)
        if X == 'A11': p300.move_to(A11_p300_bead_side)
        protocol.delay(minutes=0.1)
        p300.aspirate(20, rate=0.2)
        p300.move_to(sample_plate_mag[X].top(z=2))
        p300.default_speed = 400
        p300.dispense(200, Liquid_trash_1)
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A9'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(RemoveSup-20, rate=0.25)
        p300.default_speed = 5
        if X == 'A7': p300.move_to(A7_p300_bead_side)
        if X == 'A9': p300.move_to(A9_p300_bead_side)
        if X == 'A11': p300.move_to(A11_p300_bead_side)
        protocol.delay(minutes=0.1)
        p300.aspirate(20, rate=0.2)
        p300.move_to(sample_plate_mag[X].top(z=2))
        p300.default_speed = 400
        p300.dispense(200, Liquid_trash_1)
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A11'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(RemoveSup-20, rate=0.25)
        p300.default_speed = 5
        if X == 'A7': p300.move_to(A7_p300_bead_side)
        if X == 'A9': p300.move_to(A9_p300_bead_side)
        if X == 'A11': p300.move_to(A11_p300_bead_side)
        protocol.delay(minutes=0.1)
        p300.aspirate(20, rate=0.2)
        p300.move_to(sample_plate_mag[X].top(z=2))
        p300.default_speed = 400
        p300.dispense(200, Liquid_trash_1)
        p300.move_to(bypass)
        p300.drop_tip()

    protocol.comment('--> Repeating 2 washes')
    washreps = 2
    for wash in range(washreps):
        protocol.comment('--> ETOH Wash #'+str(wash+1))
        ETOHMaxVol = 150
        if samplecolumns >= 1:  # -------------------------------------------------
            X = 'A1'
            p300.pick_up_tip(ETOH_washtip_1)
            p300.aspirate(ETOHMaxVol, EtOH_1)
            if X == 'A7': p300.move_to(A7_p300_bead_side)
            if X == 'A9': p300.move_to(A9_p300_bead_side)
            if X == 'A11': p300.move_to(A11_p300_bead_side)
            p300.dispense(ETOHMaxVol-50, rate=0.5)
            p300.move_to(sample_plate_mag[X].center())
            p300.dispense(50, rate=0.5)
            p300.move_to(sample_plate_mag[X].top(z=2))
            p300.default_speed = 5
            p300.move_to(sample_plate_mag[X].top(z=-2))
            p300.default_speed = 400
            p300.move_to(bypass)
            protocol.pause("TIP CHECK - once per wash")
            p300.return_tip()
        if samplecolumns >= 2:  # -------------------------------------------------
            X = 'A9'
            p300.pick_up_tip(ETOH_washtip_2)
            p300.aspirate(ETOHMaxVol, EtOH_2)
            if X == 'A7': p300.move_to(A7_p300_bead_side)
            if X == 'A9': p300.move_to(A9_p300_bead_side)
            if X == 'A11': p300.move_to(A11_p300_bead_side)
            p300.dispense(ETOHMaxVol-50, rate=0.5)
            p300.move_to(sample_plate_mag[X].center())
            p300.dispense(50, rate=0.5)
            p300.move_to(sample_plate_mag[X].top(z=2))
            p300.default_speed = 5
            p300.move_to(sample_plate_mag[X].top(z=-2))
            p300.default_speed = 400
            p300.move_to(bypass)
            p300.return_tip()
        if samplecolumns >= 3:  # -------------------------------------------------
            X = 'A11'
            p300.pick_up_tip(ETOH_washtip_3)
            p300.aspirate(ETOHMaxVol, EtOH_3)
            if X == 'A7': p300.move_to(A7_p300_bead_side)
            if X == 'A9': p300.move_to(A9_p300_bead_side)
            if X == 'A11': p300.move_to(A11_p300_bead_side)
            p300.dispense(ETOHMaxVol-50, rate=0.5)
            p300.move_to(sample_plate_mag[X].center())
            p300.dispense(50, rate=0.5)
            p300.move_to(sample_plate_mag[X].top(z=2))
            p300.default_speed = 5
            p300.move_to(sample_plate_mag[X].top(z=-2))
            p300.default_speed = 400
            p300.move_to(bypass)
            p300.return_tip()

        protocol.delay(minutes=0.5)

        protocol.comment('--> Remove ETOH Wash #'+str(wash+1))
        if samplecolumns >= 1:  # -------------------------------------------------
            X = 'A7'
            p300.pick_up_tip(ETOH_removetip_1)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(ETOHMaxVol, rate=0.25)
            p300.dispense(ETOHMaxVol, Liquid_trash_1)
            protocol.pause("TIP CHECK - once per wash")
            p300.move_to(bypass)
            p300.return_tip()
        if samplecolumns >= 2:  # -------------------------------------------------
            X = 'A9'
            p300.pick_up_tip(ETOH_removetip_2)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(ETOHMaxVol, rate=0.25)
            p300.dispense(ETOHMaxVol, Liquid_trash_1)
            p300.move_to(bypass)
            p300.return_tip()
        if samplecolumns >= 3:  # -------------------------------------------------
            X = 'A11'
            p300.pick_up_tip(ETOH_removetip_3)
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(ETOHMaxVol, rate=0.25)
            p300.dispense(ETOHMaxVol, Liquid_trash_1)
            p300.move_to(bypass)
            p300.return_tip()
        wash += 1

    protocol.comment('--> Removing Residual ETOH')
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A7'
        p20.pick_up_tip()
        p20.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p20.aspirate(20, rate=0.25)
        p20.move_to(bypass)
        p20.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A9'
        p20.pick_up_tip()
        p20.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p20.aspirate(20, rate=0.25)
        p20.move_to(bypass)
        p20.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A11'
        p20.pick_up_tip()
        p20.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p20.aspirate(20, rate=0.25)
        p20.move_to(bypass)
        p20.drop_tip()

    mag_block.engage(height_from_base=6)
    protocol.comment('AIR DRY')
    protocol.delay(minutes=0.5)

    protocol.comment('MAGNET DISENGAGE')
    mag_block.disengage()

    protocol.comment('Adding RSB')
    PCRVol = 32
    PCRMixRep = 5
    PCRMixVol = 25
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A1'
        p300.pick_up_tip()
        p300.aspirate(PCRVol, Master_Tube_PCR_1.bottom(p300_offset_Temp))
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        p300.default_speed = 5
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc3)
        if X == 'A3': p300.move_to(A3_p300_loc3)
        if X == 'A5': p300.move_to(A5_p300_loc3)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        reps = 5
        for x in range(reps):
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(PCRVol, rate=0.5)
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(PCRVol, rate=1)
        reps = 3
        for x in range(reps):
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc1)
            if X == 'A3': p300.move_to(A3_p300_loc1)
            if X == 'A5': p300.move_to(A5_p300_loc1)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc3)
            if X == 'A3': p300.move_to(A3_p300_loc3)
            if X == 'A5': p300.move_to(A5_p300_loc3)
            p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag.wells_by_name()[X].bottom(z=p300_offset_Mag))
        p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag.wells_by_name()[X].top())
        protocol.delay(seconds=0.5)
        p300.move_to(sample_plate_mag.wells_by_name()[X].center())
        p300.default_speed = 400
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A3'
        p300.pick_up_tip()
        p300.aspirate(PCRVol, Master_Tube_PCR_1.bottom(p300_offset_Temp))
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        p300.default_speed = 5
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc3)
        if X == 'A3': p300.move_to(A3_p300_loc3)
        if X == 'A5': p300.move_to(A5_p300_loc3)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        reps = 5
        for x in range(reps):
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(PCRVol, rate=0.5)
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(PCRVol, rate=1)
        reps = 3
        for x in range(reps):
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc1)
            if X == 'A3': p300.move_to(A3_p300_loc1)
            if X == 'A5': p300.move_to(A5_p300_loc1)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc3)
            if X == 'A3': p300.move_to(A3_p300_loc3)
            if X == 'A5': p300.move_to(A5_p300_loc3)
            p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag.wells_by_name()[X].bottom(z=p300_offset_Mag))
        p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag.wells_by_name()[X].top())
        protocol.delay(seconds=0.5)
        p300.move_to(sample_plate_mag.wells_by_name()[X].center())
        p300.default_speed = 400
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A5'
        p300.pick_up_tip()
        p300.aspirate(PCRVol, Master_Tube_PCR_1.bottom(p300_offset_Temp))
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        p300.default_speed = 5
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc3)
        if X == 'A3': p300.move_to(A3_p300_loc3)
        if X == 'A5': p300.move_to(A5_p300_loc3)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc2)
        if X == 'A3': p300.move_to(A3_p300_loc2)
        if X == 'A5': p300.move_to(A5_p300_loc2)
        p300.dispense(PCRVol/5, rate=0.75)
        if X == 'A1': p300.move_to(A1_p300_loc1)
        if X == 'A3': p300.move_to(A3_p300_loc1)
        if X == 'A5': p300.move_to(A5_p300_loc1)
        p300.dispense(PCRVol/5, rate=0.75)
        reps = 5
        for x in range(reps):
            p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag))
            p300.aspirate(PCRVol, rate=0.5)
            if X == 'A1': p300.move_to(A1_p300_bead_top)
            if X == 'A3': p300.move_to(A3_p300_bead_top)
            if X == 'A5': p300.move_to(A5_p300_bead_top)
            p300.dispense(PCRVol, rate=1)
        reps = 3
        for x in range(reps):
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc1)
            if X == 'A3': p300.move_to(A3_p300_loc1)
            if X == 'A5': p300.move_to(A5_p300_loc1)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc2)
            if X == 'A3': p300.move_to(A3_p300_loc2)
            if X == 'A5': p300.move_to(A5_p300_loc2)
            p300.mix(PCRMixRep, PCRMixVol)
            if X == 'A1': p300.move_to(A1_p300_loc3)
            if X == 'A3': p300.move_to(A3_p300_loc3)
            if X == 'A5': p300.move_to(A5_p300_loc3)
            p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag.wells_by_name()[X].bottom(z=p300_offset_Mag))
        p300.mix(PCRMixRep, PCRMixVol)
        p300.move_to(sample_plate_mag.wells_by_name()[X].top())
        protocol.delay(seconds=0.5)
        p300.move_to(sample_plate_mag.wells_by_name()[X].center())
        p300.default_speed = 400
        p300.drop_tip()

    protocol.delay(minutes=2)

    protocol.comment('MAGNET ENGAGE')
    mag_block.engage(height_from_base=10)

    protocol.delay(minutes=4)

    protocol.comment('--> Transferring Supernatant')
    TransferSup = 30
    if samplecolumns >= 1:  # -------------------------------------------------
        X = 'A7'
        Y = 'A8'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(TransferSup, rate=0.25)
        p300.dispense(TransferSup+5, sample_plate_mag[Y].bottom(z=p300_offset_Mag))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 2:  # -------------------------------------------------
        X = 'A9'
        Y = 'A10'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(TransferSup, rate=0.25)
        p300.dispense(TransferSup+5, sample_plate_mag[Y].bottom(z=p300_offset_Mag))
        p300.move_to(bypass)
        p300.drop_tip()
    if samplecolumns >= 3:  # -------------------------------------------------
        X = 'A11'
        Y = 'A12'
        p300.pick_up_tip()
        p300.move_to(sample_plate_mag[X].bottom(z=p300_offset_Mag+4))
        p300.aspirate(TransferSup, rate=0.25)
        p300.dispense(TransferSup+5, sample_plate_mag[Y].bottom(z=p300_offset_Mag))
        p300.move_to(bypass)
        p300.drop_tip()

    protocol.comment('MAGNET DISENGAGE')
    mag_block.disengage()

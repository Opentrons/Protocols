from opentrons import protocol_api

metadata = {
    "protocolName": "Custom CSV Mass Spec Sample Prep",
    "author": "Sakib <sakib.hossain@opentrons.com>",
    "description": "Custom Protocol Request",
    "apiLevel": "2.11",
}


def run(ctx):

    [
        csv_file,
        sample_vol,
        mecn_transfer,
        mecn_vol,
        p300_mount,
        m300_mount,
        blow_out_after_dispense,
        asp_rate,
        disp_rate,
        asp_height,
        disp_height,
        mecn_asp_height,
        mecn_disp_height,
    ] = get_values(  # noqa: F821
        "csv_file",
        "sample_vol",
        "mecn_transfer",
        "mecn_vol",
        "p300_mount",
        "m300_mount",
        "blow_out_after_dispense",
        "asp_rate",
        "disp_rate",
        "asp_height",
        "disp_height",
        "mecn_asp_height",
        "mecn_disp_height",
    )

    transfer_info = [
        [val.strip().lower() for val in line.split(",")]
        for line in csv_file.splitlines()
        if line.split(",")[0].strip()
    ][1:]

    columns = len(transfer_info[0])

    # Load Labware
    tuberack = "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap"
    well_plate = "thermofisherwebseal_96_wellplate_1000ul"
    tiprack1 = ctx.load_labware("opentrons_96_tiprack_300ul", 8)
    tiprack2 = ctx.load_labware("opentrons_96_tiprack_300ul", 9)
    reservoir = ctx.load_labware("axygen_1_reservoir_90ml", 7)

    if columns == 5:
        for line in transfer_info:
            s_slot, d_slot = line[1] + line[3]
            for rack, plate in zip([s_slot], [d_slot]):
                if not int(rack) in ctx.loaded_labwares:
                    ctx.load_labware(tuberack, rack)
                if not int(plate) in ctx.loaded_labwares:
                    ctx.load_labware(well_plate, plate)
    elif columns == 7:
        for line in transfer_info:
            s_slot, d1_slot, d2_slot = line[1] + line[3] + line[5]
            for rack, plate1, plate2 in zip([s_slot], [d1_slot], [d2_slot]):
                if not int(rack) in ctx.loaded_labwares:
                    ctx.load_labware(tuberack, rack)
                if not int(plate1) in ctx.loaded_labwares:
                    ctx.load_labware(well_plate, plate1)
                if not int(plate2) in ctx.loaded_labwares:
                    ctx.load_labware(well_plate, plate2)
    else:
        raise ValueError("Invalid CSV File Format. Check your CSV file.")

    # Load Pipettes
    p300 = ctx.load_instrument(
        "p300_single_gen2", p300_mount, tip_racks=[tiprack1])
    m300 = ctx.load_instrument(
        "p300_multi_gen2", m300_mount, tip_racks=[tiprack2])

    # Helper Functions
    def pick_up(pip, loc=None):
        try:
            if loc:
                pip.pick_up_tip(loc)
            else:
                pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Please replace the empty tip racks!")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def preWet(pipette, volume, location, reps):
        ctx.comment(f"Pre-Wetting the tip(s) with {volume} uL at {location}")
        for _ in range(reps):
            pipette.aspirate(volume, location)
            pipette.dispense(volume, location)

    # Protocol Steps
    p300.flow_rate.aspirate = asp_rate
    p300.flow_rate.dispense = disp_rate
    m300.flow_rate.aspirate = asp_rate
    m300.flow_rate.dispense = disp_rate

    # One Plate
    if columns == 5:
        for line in transfer_info:
            s_slot, s_well, d1_slot, d1_well = line[1:5]
            source = ctx.loaded_labwares[int(s_slot)].wells()[int(s_well) - 1]
            dest1 = ctx.loaded_labwares[int(d1_slot)][d1_well.upper()]

            pick_up(p300)
            p300.aspirate(sample_vol, source.bottom(asp_height))
            p300.air_gap(20)
            p300.dispense(sample_vol + 20, dest1.bottom(disp_height))
            if blow_out_after_dispense:
                p300.blow_out(dest1)
            p300.drop_tip()

    # Two Plates
    if columns == 7:
        for line in transfer_info:
            s_slot, s_well, d1_slot, d1_well, d2_slot, d2_well = line[1:7]
            source = ctx.loaded_labwares[int(s_slot)].wells()[int(s_well) - 1]
            dest1 = ctx.loaded_labwares[int(d1_slot)][d1_well.upper()]
            dest2 = ctx.loaded_labwares[int(d2_slot)][d2_well.upper()]

            pick_up(p300)
            p300.aspirate(sample_vol, source.bottom(asp_height))
            p300.air_gap(20)
            p300.dispense(sample_vol + 20, dest1.bottom(disp_height))
            if blow_out_after_dispense:
                p300.blow_out(dest1)
            p300.aspirate(sample_vol, source.bottom(asp_height))
            p300.air_gap(20)
            p300.dispense(sample_vol + 20, dest2.bottom(disp_height))
            if blow_out_after_dispense:
                p300.blow_out(dest2)
            p300.drop_tip()

    # Acetonitrile (MeCN) Transfer
    if mecn_transfer:
        if columns == 5:
            pick_up(m300)
            preWet(m300, 100, reservoir["A1"], 1)
            for col in ctx.loaded_labwares[3].rows()[0]:
                m300.aspirate(
                    mecn_vol, reservoir["A1"].bottom(mecn_asp_height))
                m300.dispense(mecn_vol, col.bottom(mecn_disp_height))
                if blow_out_after_dispense:
                    m300.blow_out(col)
            m300.drop_tip()

        if columns == 7:
            pick_up(m300)
            preWet(m300, 100, reservoir["A1"], 1)
            for col1, col2 in zip(
                ctx.loaded_labwares[3].rows(
                )[0], ctx.loaded_labwares[6].rows()[0]
            ):
                m300.aspirate(
                    mecn_vol, reservoir["A1"].bottom(mecn_asp_height))
                m300.dispense(mecn_vol, col1.bottom(mecn_disp_height))
                if blow_out_after_dispense:
                    m300.blow_out(col1)
                m300.aspirate(
                    mecn_vol, reservoir["A1"].bottom(mecn_asp_height))
                m300.dispense(mecn_vol, col2.bottom(mecn_disp_height))
                if blow_out_after_dispense:
                    m300.blow_out(col2)
            m300.drop_tip()
